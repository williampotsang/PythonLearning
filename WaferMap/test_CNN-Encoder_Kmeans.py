# pip install opencv-python
import cv2
print(" opencv-python " + cv2.__version__)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans

# conda install -c anaconda keras
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from keras import backend as K
print(" keras " + keras.__version__)


### Read Data
df1 = pd.read_pickle(".\WaferMap\wafermap1.pkl")
df2 = pd.read_pickle(".\WaferMap\wafermap2.pkl")
df3 = pd.read_pickle(".\WaferMap\wafermap3.pkl")
df = pd.concat([df1,df2,df3])
print(df1.head())
print(df.info())


### Calculate pic dimension and define wafer map type
def find_dim(x):
    dim0 = np.size(x,axis=0)
    dim1 = np.size(x,axis=1)
    return dim0, dim1
df['waferMapDim']=df.waferMap.apply(find_dim)


### Add 2 columns for Num of Failure & Test Lable
df['failureNum']   =df.failureType
mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
df['trainTestNum'] =df.trianTestLabel
mapping_traintest = {'Training':0,'Test':1}
# mapping
df = df.replace({'failureNum':mapping_type, 'trainTestNum':mapping_traintest})


### Get size 26*26 as new dataset
df['waferMapDim_tt'] = df.waferMapDim
#只取具有完整維度26*26的資料
for i in range(len(df)):
    if df['waferMapDim'][i][0] == df['waferMapDim'][i][1] == 26:
        df['waferMapDim_tt'][i] = 0
    else:
        df['waferMapDim_tt'][i] = 1
#只取具有完整維度26*26的資料
df_map26 = df[df['waferMapDim_tt']==0]
df_map26 = df_map26.reset_index()
print(df_map26.info())
print(df_map26.head())


# 只取failnum被mapping到的record
def fail_t(x):
    if type(x) != int:
        result = "N"
    else:
        result = "Y"
    return result
df_map26['fail_t']=df_map26.failureNum.apply(fail_t)
df_map26_withlabel = df_map26[df_map26['fail_t'] == 'Y'].reset_index()
print(df_map26_withlabel.head())
print(df_map26_withlabel.info())



# 擴大wafermap_t從26 x 26 變成 28 x 28(周圍補零)
def add_zero(x):
    zero1 = np.zeros(26)
    zero2 = np.zeros(28)
    new = np.column_stack((zero1,x,zero1))
    new2 = np.row_stack((zero2,new,zero2))
    return new2
df_map26_withlabel['waferMap_t']=df_map26_withlabel.waferMap.apply(add_zero)
'''
def one_to_zero(x):
    if x == 1:
        result = 0
    return result
'''
# 把die value 從 1/2 換成 0/1
for i in range(len(df_map26_withlabel)):
    for j in range(28):
        for k in range(28):
            if df_map26_withlabel['waferMap_t'][i][j][k] == 1:
                df_map26_withlabel['waferMap_t'][i][j][k] = 0
            elif df_map26_withlabel['waferMap_t'][i][j][k] == 2:
                df_map26_withlabel['waferMap_t'][i][j][k] = 1
print(df_map26_withlabel.head())
print(df_map26_withlabel['waferMap_t'][0])

## resahpe data, 每個die多長一個維度(深度)
wafer_data = np.stack(df_map26_withlabel.waferMap_t.to_numpy())
wafer_data = wafer_data.reshape(wafer_data.shape[0], 28, 28, 1)



#########################################
### CNN
#########################################
model = Sequential()

# Encoder ------------------------
#1st convolution layer
model.add(Conv2D(16, (5, 5),  #16 is number of filters and (3, 3) is the size of the filter.
          padding='same', input_shape=(28,28,1)))
model.add(Activation('relu'))
model.add(Conv2D(16,(5, 5), padding='same')) # apply 2 filters sized of (3x3)
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2), padding='same'))

#2nd convolution layer
model.add(Conv2D(8,(5, 5), padding='same')) # apply 2 filters sized of (3x3)
model.add(Activation('relu'))
model.add(Conv2D(8,(5, 5), padding='same')) # apply 2 filters sized of (3x3)
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2), padding='same'))

# Decoder -------------------------         
#3rd convolution layer
model.add(Conv2D(8,(5, 5), padding='same')) # apply 2 filters sized of (3x3)
model.add(Activation('relu'))
model.add(UpSampling2D((2, 2)))
 
#4rd convolution layer
model.add(Conv2D(16,(5, 5), padding='same'))
model.add(Activation('relu'))
model.add(UpSampling2D((2, 2)))
#-------------------------
 
model.add(Conv2D(1,(3, 3), padding='same'))
model.add(Activation('sigmoid'))
print(model.summary())
 
model.compile(optimizer='adam', loss='binary_crossentropy')
model.fit(wafer_data, wafer_data, epochs=10)



#########################################
### Predict(Decode)
#########################################
decoded_imgs = model.predict(wafer_data)
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # 显示原本的图像
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(wafer_data[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)

     # 显示重构后的图像
    ax = plt.subplot(2, n, i+1+n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)
plt.show()



#######################
### 'Edge-Loc':2
#######################
### mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
#df_map26_withlabel[df_map26_withlabel['failureNum']==2].head()

## resahpe data, 每個die多長一個維度(深度)
wafer_data_2 = np.stack(df_map26_withlabel[df_map26_withlabel['failureNum']==2].waferMap_t.to_numpy())
wafer_data_2 = wafer_data_2.reshape(wafer_data_2.shape[0], 28, 28, 1)

### Predict(Decode)
decoded_imgs = model.predict(wafer_data_2)

n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # 显示原本的图像
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(wafer_data_2[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)

     # 显示重构后的图像
    ax = plt.subplot(2, n, i+1+n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)
plt.show()

#######################
### ''Edge-Ring':3
#######################
### mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
#df_map26_withlabel[df_map26_withlabel['failureNum']==3].head()

## resahpe data, 每個die多長一個維度(深度)
wafer_data_3 = np.stack(df_map26_withlabel[df_map26_withlabel['failureNum']==3].waferMap_t.to_numpy())
wafer_data_3 = wafer_data_3.reshape(wafer_data_3.shape[0], 28, 28, 1)

### Predict(Decode)
decoded_imgs = model.predict(wafer_data_3)

n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # 显示原本的图像
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(wafer_data_3[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)

     # 显示重构后的图像
    ax = plt.subplot(2, n, i+1+n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)
plt.show()

#######################
### 'Scratch':6
#######################
### mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
#df_map26_withlabel[df_map26_withlabel['failureNum']==6].head()

## resahpe data, 每個die多長一個維度(深度)
wafer_data_6 = np.stack(df_map26_withlabel[df_map26_withlabel['failureNum']==6].waferMap_t.to_numpy())
wafer_data_6 = wafer_data_6.reshape(wafer_data_6.shape[0], 28, 28, 1)

### Predict(Decode)
decoded_imgs = model.predict(wafer_data_6)

n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # 显示原本的图像
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(wafer_data_6[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)

     # 显示重构后的图像
    ax = plt.subplot(2, n, i+1+n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)

plt.suptitle("'Scratch':6")
plt.show()
####################################################################################################

# layer[7] is activation_3 (Activation), it is compressed representation
get_3rd_layer_output = K.function([model.layers[0].input], [model.layers[7].output])
compressed = get_3rd_layer_output([wafer_data])[0]
compressed.shape
compressed[1,:,:,0]

'''
### 劃出特徵圖
### mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
#df_map26_withlabel[df_map26_withlabel['failureNum']==6].head()

## resahpe data, 每個die多長一個維度(深度)
wafer_data_6 = np.stack(df_map26_withlabel[df_map26_withlabel['failureNum']==0].waferMap_t.to_numpy())
wafer_data_6 = wafer_data_6.reshape(wafer_data_6.shape[0], 28, 28, 1)
compressed = get_3rd_layer_output([wafer_data_6])[0]

n = 10
plt.figure(figsize=(20, 10))
for i in range(n):
     # 显示原本的图像
    ax = plt.subplot(6, n, i + 1)
    plt.imshow(wafer_data_6[i].reshape(28, 28))
    
    # 显示重构后的图像
    ax = plt.subplot(6, n, i+1+n*1)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    
    # Featrure 0
    ax = plt.subplot(6, n, i+1+n*2)
    plt.imshow(compressed[i,:,:,0])
  
     # Featrure 1
    ax = plt.subplot(6, n, i+1+n*3)
    plt.imshow(compressed[i,:,:,1])
   
     # Featrure 2
    ax = plt.subplot(6, n, i+1+n*4)
    plt.imshow(compressed[i,:,:,2])
    
     # Featrure 3
    ax = plt.subplot(6, n, i+1+n*5)
    plt.imshow(compressed[i,:,:,3])
    
plt.suptitle("'Center':0   Before, Decoder(After) & Encoder" )
plt.show()
'''


###############################################################################################################################
### mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
###############################################################################################################################
plt.suptitle("'Center':0   Before, Decoder(After) & Encoder" )

## resahpe data, 每個die多長一個維度(深度)
wafer_data_6 = np.stack(df_map26_withlabel[df_map26_withlabel['failureNum']==6].waferMap_t.to_numpy())
wafer_data_6 = wafer_data_6.reshape(wafer_data_6.shape[0], 28, 28, 1)

### Predict(Decode)
decoded_imgs = model.predict(wafer_data_6)

### 計算特徵圖 ###
#layer[7] is activation_3 (Activation), it is compressed representation
get_3rd_layer_output = K.function([model.layers[0].input], [model.layers[14].output])
compressed = get_3rd_layer_output([wafer_data_6])[0]

# 設定每行(row)顯示的片數
iPlotWfrCount=10

# 显示原本的图像
fig,ax = plt.subplots(1,iPlotWfrCount,figsize=(20,20))
ax = ax.ravel(order='C')
for iWfr in  range(iPlotWfrCount):
    #ax[iWfr].imshow(wafer_data_6[iWfr].reshape(28, 28),vmin=0, vmax=2,cmap='viridis')
    ax[iWfr].imshow(wafer_data_6[iWfr].reshape(28, 28))
plt.tight_layout()
plt.show()

# 显示重构后的图像
fig,ax = plt.subplots(1,iPlotWfrCount,figsize=(20,20))
ax = ax.ravel(order='C')
for iWfr in  range(iPlotWfrCount):
    #ax[iWfr].imshow(decoded_imgs[iWfr].reshape(28, 28),vmin=0, vmax=2,cmap='viridis')
    ax[iWfr].imshow(decoded_imgs[iWfr].reshape(28, 28))
plt.tight_layout()
plt.show()

# Featrure i 
for iFeature in range(compressed.shape[3]): 
    fig,ax = plt.subplots(1,iPlotWfrCount,figsize=(20,20))
    ax = ax.ravel(order='C')
    
    for iWfr in  range(iPlotWfrCount):
        #ax[iWfr].imshow(compressed[iWfr,:,:,iFeature],vmin=0, vmax=2,cmap='viridis')
        ax[iWfr].imshow(compressed[iWfr,:,:,iFeature])
    
    plt.tight_layout()
    plt.show()
    
compressed.shape


'''
#layer[7] is size of (None, 7, 7, 2). this means 2 different 7x7 sized matrixes. We will flatten these matrixes.
compressed = compressed.reshape(compressed.shape[0],7*7*16)
'''
################################################################
######### Cluster 操作 #########
################################################################
get_3rd_layer_output = K.function([model.layers[0].input], [model.layers[14].output])
compressed = get_3rd_layer_output([wafer_data])[0]
compressed = compressed.reshape(compressed.shape[0],compressed.shape[1]*compressed.shape[2]*compressed.shape[3])
print(compressed.shape)

m = 30
data = compressed
kmeans = KMeans(n_clusters=m,init='k-means++')
kmeans.fit(data)
Z = kmeans.predict(data)
print(Z.shape)
print(Z[1])


for i in range(m):
    row = np.where(Z==i)[0]  # row in Z for elements of cluster i
    num = row.shape[0]       #  number of elements for each cluster

    print("cluster "+str(i))
    print(str(num)+" elements")

    fig,ax = plt.subplots(1,5,figsize=(20,20))
    ax = ax.ravel(order='C')
    for i in  range(5):
        df_loc = row[i] 
        img = df_map26_withlabel.waferMap.iloc[df_loc]
        ax[i].imshow(img,vmin=0, vmax=2,cmap='viridis')
    plt.tight_layout()
    plt.show()

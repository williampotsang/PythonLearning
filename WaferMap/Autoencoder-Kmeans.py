#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from keras import backend as K


### Read Data
df1 = pd.read_pickle("wafermap1.pkl")
df2 = pd.read_pickle("wafermap2.pkl")
df3 = pd.read_pickle("wafermap3.pkl")
df = pd.concat([df1,df2,df3])

### Calculate pic dimension and define wafer map type
def find_dim(x):
    dim0 = np.size(x,axis=0)
    dim1 = np.size(x,axis=1)
    return dim0, dim1

df['waferMapDim']=df.waferMap.apply(find_dim)

df['failureNum']=df.failureType
df['trainTestNum']=df.trianTestLabel
mapping_type = {'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
mapping_traintest = {'Training':0,'Test':1}

df = df.replace({'failureNum':mapping_type, 'trainTestNum':mapping_traintest})


### Get size 26*26 as new dataset
df['waferMapDim_tt'] = df.waferMapDim

for i in range(len(df)):
    if df['waferMapDim'][i][0] == df['waferMapDim'][i][1] == 26:
        df['waferMapDim_tt'][i] = 0
    else:
        df['waferMapDim_tt'][i] = 1

df_map26 = df[df['waferMapDim_tt']==0]
df_map26 = df_map26.reset_index()


def fail_t(x):
    if type(x) != int:
        result = "N"
    else:
        result = "Y"
    return result

df_map26['fail_t']=df_map26.failureNum.apply(fail_t)

df_map26_withlabel = df_map26[df_map26['fail_t'] == 'Y'].reset_index()

def add_zero(x):
    zero1 = np.zeros(26)
    zero2 = np.zeros(28)
    new = np.column_stack((zero1,x,zero1))
    new2 = np.row_stack((zero2,new,zero2))
    return new2

df_map26_withlabel['waferMap_t']=df_map26_withlabel.waferMap.apply(add_zero)


def one_to_zero(x):
    if x == 1:
        result = 0
    return result

for i in range(len(df_map26_withlabel)):
    for j in range(28):
        for k in range(28):
            if df_map26_withlabel['waferMap_t'][i][j][k] == 1:
                df_map26_withlabel['waferMap_t'][i][j][k] = 0
            elif df_map26_withlabel['waferMap_t'][i][j][k] == 2:
                df_map26_withlabel['waferMap_t'][i][j][k] = 1


# In[2]:


## resahpe data
wafer_data = np.stack(df_map26_withlabel.waferMap_t.to_numpy())
wafer_data = wafer_data.reshape(wafer_data.shape[0], 28, 28, 1)


# In[ ]:


model = Sequential()
 
#1st convolution layer
model.add(Conv2D(16, (5, 5) #16 is number of filters and (3, 3) is the size of the filter.
    , padding='same', input_shape=(28,28,1)))
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

#-------------------------
     
    
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


# In[ ]:


decoded_imgs = model.predict(wafer_data)

n = 10

plt.figure(figsize=(20, 4))
for i in range(n):
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


# In[ ]:





# In[ ]:





# In[ ]:


#layer[7] is activation_3 (Activation), it is compressed representation
get_3rd_layer_output = K.function([model.layers[0].input], [model.layers[7].output])
compressed = get_3rd_layer_output([wafer_data])[0]
#layer[7] is size of (None, 7, 7, 2). this means 2 different 7x7 sized matrixes. We will flatten these matrixes.
compressed = compressed.reshape(compressed.shape[0],7*7*16)


# In[ ]:


m = 30
data = compressed
kmeans = KMeans(n_clusters=m,init='k-means++')
kmeans.fit(data)
Z = kmeans.predict(data)
for i in range(m):
    row = np.where(Z==i)[0]  # row in Z for elements of cluster i
    num = row.shape[0]       #  number of elements for each cluster

    print("cluster "+str(i))
    print(str(num)+" elements")

    fig,ax = plt.subplots(1,5,figsize=(20,20))
    ax = ax.ravel(order='C')
    for i in range(5):
        df_loc = row[i] 
        img = df_map26_withlabel.waferMap.iloc[df_loc]
        ax[i].imshow(img,vmin=0, vmax=2,cmap='viridis')
    plt.tight_layout()
    plt.show()


# In[ ]:





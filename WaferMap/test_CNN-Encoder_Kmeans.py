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






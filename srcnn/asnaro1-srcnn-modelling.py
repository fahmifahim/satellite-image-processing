asnaro1-srcnn-modelling.py
import os, json, requests, math
from skimage import io
from io import BytesIO
import matplotlib.pyplot as plt
import warnings
import random
import numpy as np

#%matplotlib inline

#from keras import backend as K
from keras import backend as K
from keras.models import Sequential, Model, load_model
from keras.layers import Input, Dense, Input, Conv2D, Conv2DTranspose, MaxPooling2D, UpSampling2D, Lambda, Activation, Flatten, Add
from keras.optimizers import Adam, SGD
from keras.preprocessing.image import array_to_img, img_to_array, load_img,ImageDataGenerator

def drop_resolution(x,scale):
   #画像のサイズをいったん縮小したのちに再び拡大することで、低解像度の画像を作る。
   size=(x.shape[0],x.shape[1])
   small_size=(int(size[0]/scale),int(size[1]/scale))
   img=array_to_img(x)
   small_img=img.resize(small_size, 3)
   return img_to_array(small_img.resize(img.size,3))

def data_generator(data_dir,mode,scale,target_size=(256,256),batch_size=32,shuffle=True):
   for imgs in ImageDataGenerator().flow_from_directory(
       directory=data_dir,
       classes=[mode],
       class_mode=None,
       color_mode='rgb',
       target_size=target_size,
       batch_size=batch_size,
       shuffle=shuffle
   ):
       x=np.array([
           drop_resolution(img,scale) for img in imgs
           ])
       yield x/255.,imgs/255.


DATA_DIR='./Data_ASNARO1_SRCNN/'
N_TRAIN_DATA=6000 #学習用データ数
N_TEST_DATA=616   #評価用データ数
BATCH_SIZE=32     #バッチサイズ

train_data_generator=data_generator(
   DATA_DIR,'train', scale=4.0, batch_size=BATCH_SIZE
)

test_x,test_y=next(
   data_generator(
   DATA_DIR,'test',scale=4.0, batch_size=N_TEST_DATA,shuffle=False
   )
)

model = Sequential()

model.add(Conv2D(filters=64, kernel_size= 9, activation='relu', padding='same', input_shape=(None,None,3)))
model.add(Conv2D(filters=32, kernel_size= 1, activation='relu', padding='same'))
model.add(Conv2D(filters=3, kernel_size= 5, padding='same'))

model.summary()

def psnr(y_true,y_pred):
    return -10*K.log(K.mean(K.flatten((y_true-y_pred))**2)
    )/np.log(10)

model.compile(
    loss='mean_squared_error',
    optimizer= 'adam',
    metrics=[psnr]
)

model.fit(
    train_data_generator,
    validation_data=(test_x,test_y),
    steps_per_epoch=N_TRAIN_DATA//BATCH_SIZE,
    #epochs=200
    epochs=10
)

#model save  : model.save(config.MODEL_PATH, overwrite = True)
#keras stop :

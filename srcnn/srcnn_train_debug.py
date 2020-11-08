import os

import numpy as np
import pdb

from keras import backend as K
from keras.models import Sequential
from keras.layers import Conv2D
from keras.preprocessing.image \
    import array_to_img, img_to_array, ImageDataGenerator


def psnr(y_true, y_pred):
    return -10 * \
        K.log(K.mean(K.flatten((y_true - y_pred))**2)) / np.log(10)


def drop_resolution(x, scale):
    # 画像のサイズをいったん縮小したのちに再び拡大することで、低解像度の画像を作る。
    size = (x.shape[0], x.shape[1])
    print("----- print size:drop_resolution")
    print(size)
    pdb.set_trace()

    small_size = (int(size[0] / scale), int(size[1] / scale))
    print("----- print small_size:drop_resolution")
    print(small_size)
    pdb.set_trace()

    img = array_to_img(x)
    print("----- print img:drop_resolution")
    print(img)
    pdb.set_trace()

    small_img = img.resize(small_size, 3)
    print("----- print small_img:drop_resolution")
    print(small_img)
    pdb.set_trace()

    print("----- print small_img.resize")
    print(img_to_array(small_img.resize(img.size,3)))
    pdb.set_trace()
    
    return img_to_array(small_img.resize(img.size, 3))


def data_generator(data_dir, mode, scale,
                   target_size=(256, 256),
                   batch_size=32,
#                   batch_size=10,
                   shuffle=True):
    for imgs in ImageDataGenerator().flow_from_directory(
        directory=data_dir,
        classes=[mode],
        class_mode=None,
        color_mode='rgb',
        target_size=target_size,
        batch_size=batch_size,
        shuffle=shuffle
    ):
        x = np.array([drop_resolution(img, scale) for img in imgs])
        print("----- print x:data_generator")
        print(x)
        pdb.set_trace()
        
        yield x / 255., imgs / 255.


dataset_dir = './Data_ASNARO1_SRCNN/'
#n_train = 6000
n_train = 2000
#n_test = 616
n_test = 100
batch_size = 32
#batch_size = 8
epochs = 200

if __name__ == '__main__':

    model_filename = os.path.basename(__file__).replace('.py', '') + \
        '-ep' + str(epochs) + \
        '-bs' + str(batch_size) + \
        '.h5'
    print("---------------"+model_filename)
    pdb.set_trace()
    data_dir = 'data/'

    train_data_generator = \
        data_generator(dataset_dir, 'train', scale=4.0,
                       batch_size=batch_size, shuffle=True)
    print("train_data_generator")
    print(train_data_generator)
    pdb.set_trace()

    test_x, test_y = \
        next(data_generator(dataset_dir, 'test', scale=4.0,
                            batch_size=n_test, shuffle=False))

    model = Sequential()

    model.add(Conv2D(input_shape=(None, None, 3),
                     filters=64, kernel_size=9,
                     activation='relu', padding='same'))
    model.add(Conv2D(filters=32, kernel_size=1,
                     activation='relu', padding='same'))
    model.add(Conv2D(filters=3, kernel_size=5, padding='same'))

    model.summary()

    model.compile(
        loss='mean_squared_error',
        optimizer='adam',
        metrics=[psnr]
    )

    model.fit(train_data_generator,
              epochs=epochs,
              validation_data=(test_x, test_y),
              steps_per_epoch=n_train // batch_size)

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    model.save(data_dir + model_filename, overwrite=True)

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

    print("----- ORIGINAL input array")
    print(x)

    size = (x.shape[0], x.shape[1])
    small_size = (int(size[0] / scale), int(size[1] / scale))

    img = array_to_img(x)
    print("----- ORIGINAL img object and array")
    print(img)
    print(img_to_array(img))

    small_img = img.resize(small_size, 3)
    print("----- RESIZE small_img object and array")
    print(small_img)
    print(img_to_array(small_img))

    print("----- REPRODUCE ORIGINAL reproduce_img object and array")
    reproduce_img = small_img.resize(img.size, 3)
    print(reproduce_img)
    print(img_to_array(reproduce_img))
    
    pdb.set_trace()
    return img_to_array(reproduce_img)


def data_generator(data_dir, mode, scale,
                   target_size=(256, 256),
                   batch_size=1,
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
        print("-----data_generator:imgs")
        print(imgs)
        pdb.set_trace()

        x = np.array([drop_resolution(img, scale) for img in imgs])
        print("----- print data_generator:x")
        print(x)
        pdb.set_trace()

        yield x / 255., imgs / 255.


dataset_dir = './Data_ASNARO1_SRCNN/'
#n_train = 6000
n_train = 1
#n_test = 616
n_test = 1
batch_size = 1
#batch_size = 8
epochs = 1

if __name__ == '__main__':

    model_filename = os.path.basename(__file__).replace('.py', '') + \
        '-ep' + str(epochs) + \
        '-bs' + str(batch_size) + \
        '.h5'
    print("-----"+model_filename)
    pdb.set_trace()
    data_dir = 'data/'

    print("-----calling train_data_generator")
    #train_data_generator = data_generator(dataset_dir, 'train', scale=4.0, batch_size=batch_size, shuffle=True)
    train_data_generator = data_generator(dataset_dir, 'train', scale=1.0, batch_size=batch_size, shuffle=True)
    print(train_data_generator)
    pdb.set_trace()

    print("-----calling test_data_generator")
    #test_x, test_y = next(data_generator(dataset_dir, 'test', scale=4.0, batch_size=n_test, shuffle=False))
    test_x, test_y = next(data_generator(dataset_dir, 'test', scale=1.0, batch_size=n_test, shuffle=False))
    print("-----test_x=")
    print(test_x)
    print("-----test_y=")
    print(test_y)
    
    pdb.set_trace()

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

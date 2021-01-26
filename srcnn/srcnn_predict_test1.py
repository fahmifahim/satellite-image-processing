import os

import time
import matplotlib.pyplot as plt
import matplotlib
from keras import backend as K
matplotlib.use('Agg')

if True:
    import keras

    from srcnn_asnaro1_train \
        import dataset_dir, n_test, epochs, batch_size, psnr, data_generator

if __name__ == '__main__':

    #N_show = 319  # N_show番目の評価用データを表示
    N_show = 2  # N_show番目の評価用データを表示

    model_filename = 'srcnn_asnaro1_train' + \
        '-ep' + str(epochs) + \
        '-bs' + str(batch_size)
    print("---Model FILENAME = ", model_filename)
    path_to_model = './data/' + model_filename + '.h5'
    result_dir = 'rslt/'

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    # Time stamp
    timestr = time.strftime("%Y%m%d-%H%M%S")

    test_x, test_y = \
            next(data_generator(dataset_dir, 'test', scale=4.0,
                                batch_size=n_test, shuffle=False))

    # Print ORIGINAL and LOW RESOLUTION
    #print("--ORIGINAL--")
    #print(test_y)
    #print("--LOW RESOLUTION--")
    #print(test_x)

    # Reload a pretrained Keras model from the saved model:
    # model = keras.models.load_model(path_to_model, custom_objects=[psnr])
    model = keras.models.load_model(path_to_model,
                                    custom_objects={'psnr': psnr})

    # Check its architecture
    model.summary()
    
    # Print PREDICTION 
    #print("--PREDICTION--")
    #print(pred)

    # Calculate PSNR between ORIGINAL and PREDICTION
    print("--PSNR--")
    for i in range(len(test_y)):
        # Do the prediction
        pred[i] = model.predict(test_x[i])

        psnr_array = K.get_value(psnr(test_y[i], pred[i]))
        print(psnr_array)

        fig = plt.figure(figsize=(50, 50), facecolor="w")

        plt.subplot(1, 3, 1)
        plt.title("Original", fontsize=80)
        plt.tight_layout()
        plt.imshow(test_y[N_show, :, :])

        plt.subplot(1, 3, 2)
        plt.title("Low resolution", fontsize=80)
        plt.tight_layout()
        plt.imshow(test_x[N_show, :, :])

        plt.subplot(1, 3, 3)
        plt.title("SRCNN result", fontsize=80)
        plt.tight_layout()
        plt.imshow(pred[N_show, :, :])

        print('Saving SRCNN result image...')
        plt.savefig(result_dir + model_filename +
                    '-' + str(N_show) + '-' + timestr + '.png')
    }

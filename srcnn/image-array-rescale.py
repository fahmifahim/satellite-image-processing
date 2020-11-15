import numpy as np
from PIL import Image
from skimage.transform import resize
from keras.preprocessing.image import img_to_array, load_img, array_to_img

im_path = 'Data_ASNARO1_SRCNN/train/output_z18_103230_232831.png'
im1 = Image.open(im_path)
im2 = load_img(im_path, grayscale=False, color_mode='rgb', target_size=(256,256))
im3 = load_img(im_path, grayscale=False, color_mode='rgba', target_size=(256,256))


print("---PIL")
print(im1)
im_sequence = im1.getdata()
im_array = np.array(im_sequence)
print(im_array)


print("\n\n---KERAS")
print(im2)
im3_sequence = im3.getdata()
im3_array = img_to_array(im3_sequence)
print(im3_array)

im3_resize64 = resize(im3, (64, 64))
print(im3_resize64)

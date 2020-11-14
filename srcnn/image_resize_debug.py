import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array, load_img

im_path = 'Data_ASNARO1_SRCNN/train/output_z18_103230_232831.png'
im1 = Image.open(im_path)
im2 = load_img(im_path, grayscale=False, color_mode='rgb', target_size=(256,256))
im3 = load_img(im_path, grayscale=False, color_mode='rgba', target_size=(256,256))


print("---Original")
print(im3)
im_sequence = im3.getdata()
#im_array = np.array(im_sequence)
im_array = img_to_array(im_sequence)
print(im_array)

#im_resize256 = im.resize(size=(256,256), resample=Image.BICUBIC)
#print("---Resize256")
#print(im_resize256)
#im_sequence256 = im_resize256.getdata()
##im_array256 = np.array(im_sequence256)
#im_array256 = img_to_array(im_sequence256)
#print(im_array256)
#
#im_resize128 = im.resize(size=(128,128), resample=Image.BICUBIC)
#print("---Resize128")
#print(im_resize128)
#im_sequence128 = im_resize128.getdata()
##im_array128 = np.array(im_sequence128)
#im_array128 = img_to_array(im_sequence128)
#print(im_array128)
#
#im_resize85 = im.resize(size=(85,85), resample=Image.BICUBIC)
#print("---Resize85")
#print(im_resize85)
#im_sequence85 = im_resize85.getdata()
##im_array85 = np.array(im_sequence85)
#im_array85 = img_to_array(im_sequence85)
#print(im_array85)
#
im_resize64 = im2.resize(size=(64,64), resample=Image.BICUBIC)
print("---Resize64")
print(im_resize64)
im_sequence64 = im_resize64.getdata()
#im_array64 = np.array(im_sequence64)
im_array64 = img_to_array(im_sequence64)
print(im_array64)

from PIL import Image

#im = Image.open('original.png')
im = Image.open('Data_ASNARO1_SRCNN/train/output_z18_103230_232831.png')
print(im)

im_resize = im.resize(size=(64,64))
print(im_resize)


import numpy as np
from PIL import Image

#im = Image.open('original.png')
im = Image.open('Data_ASNARO1_SRCNN/train/output_z18_103230_232831.png')
print("---Original")
print(im)
im_sequence = im.getdata()
im_array = np.array(im_sequence)
print(im_array)
print(Image.BICUBIC)

im_resize256 = im.resize(size=(256,256), resample=Image.BICUBIC)
print("---Resize256")
print(im_resize256)
im_sequence256 = im_resize256.getdata()
im_array256 = np.array(im_sequence256)
print(im_array256)

im_resize128 = im.resize(size=(128,128), resample=Image.BICUBIC)
print("---Resize128")
print(im_resize128)
im_sequence128 = im_resize128.getdata()
im_array128 = np.array(im_sequence128)
print(im_array128)

im_resize85 = im.resize(size=(85,85), resample=Image.BICUBIC)
print("---Resize85")
print(im_resize85)
im_sequence85 = im_resize85.getdata()
im_array85 = np.array(im_sequence85)
print(im_array85)

im_resize64 = im.resize(size=(64,64), resample=Image.BICUBIC)
print("---Resize64")
print(im_resize64)
im_sequence64 = im_resize64.getdata()
im_array64 = np.array(im_sequence64)
print(im_array64)

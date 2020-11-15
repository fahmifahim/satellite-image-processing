import numpy as np
from PIL import Image
from skimage.transform import resize, rescale, downscale_local_mean
from keras.preprocessing.image import img_to_array, load_img, array_to_img

im_path = 'Data_ASNARO1_SRCNN/train/output_z18_103230_232831.png'
im1 = Image.open(im_path)
im2 = load_img(im_path, grayscale=False, color_mode='rgb', target_size=(256,256))
im3 = load_img(im_path, grayscale=False, color_mode='rgba', target_size=(256,256))


#Reference: 
#https://scikit-image.org/docs/dev/auto_examples/transform/plot_rescale.html#sphx-glr-auto-examples-transform-plot-rescale-py

print("---PIL")
print(im1)
im_sequence = im1.getdata()
im_array = np.array(im_sequence)
print(im_array)

#print("\nRESIZE ARRAY to 64")
#im_resize64 = resize(im_array,(64,64))
#print(im_resize64)

print("\n\n---KERAS")
print(im2)
im2_sequence = im2.getdata()
im2_array = img_to_array(im2_sequence)
print(im2_array)

print("\nRESIZE ARRAY to 64")
im2_resize64 = resize(im2_array, (64, 64), anti_aliasing=True)
print(im2_resize64)

print("\nRESCALE ARRAY to 64 scale factor 0.25")
im2_rescale64 = rescale(im2_array, 0.25, anti_aliasing=False)
print(im2_rescale64)

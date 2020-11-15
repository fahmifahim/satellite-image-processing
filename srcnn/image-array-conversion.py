import numpy as np
from PIL import Image
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

#new_im1 = Image.fromarray(im_array)
new_im1 = Image.fromarray(np.uint8(im_array))
print(new_im1)

print("\n\n---KERAS")
print(im2)
im3_sequence = im3.getdata()
im3_array = img_to_array(im3_sequence)
print(im3_array)

new_im3 = array_to_img(im3_array)
print(new_im3)

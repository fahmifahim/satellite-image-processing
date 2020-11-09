from PIL import Image

#im = Image.open('original.png')
im = Image.open('Data_ASNARO1_SRCNN/train/output_z18_103230_232831.png')
print(im)

im_resize = im.resize(size=(64,64))
print(im_resize)

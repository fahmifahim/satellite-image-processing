from PIL import Image

im = Image.open('original.png')

im_resize = im.resize(size=(128,128))

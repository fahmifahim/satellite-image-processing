import numpy as np
from skimage import io, color, img_as_ubyte, filters
import requests
from io import BytesIO
from keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
%matplotlib inline


# VARIABLE
## API Domain for Tellus
URL_DOMAIN = "gisapi.tellusxdp.com"
## API token
BEARER_TOKEN = "xxx"  # put your Tellus Token

## X,Y,Z coordinate for specific place you want to observe
Z = 13
X = 7276
Y = 3225

if BEARER_TOKEN == "":
    print("APIトークンがセットされていません")

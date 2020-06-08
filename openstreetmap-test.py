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
    print("API Token need to be specified")

    
def get_data(img_type, domain=URL_DOMAIN, z=Z, x=X, y=Y, query=""):
    if query != "":
        query = "?" + query

    # Set the token at header for Authorization
    res = requests.get("https://{}/{}/{}/{}/{}.png{}".format(URL_DOMAIN, img_type, z, x, y, query),
                   headers={"Authorization": "Bearer " + BEARER_TOKEN})

    # NumPy array 
    img = img_to_array(load_img(BytesIO(res.content)))
    return img.astype(np.uint8)

img_osm = get_data("osm")


print(img_osm.shape)
io.imshow(img_osm)

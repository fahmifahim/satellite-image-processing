# Reference: https://sorabatake.jp/4690/ 
# Functions: get_ASNARO_scene(), get_tile_num(), get_ASNARO_image()
# ASNARO-1 API: https://www.tellusxdp.com/market/api_reference/414

import os, json, requests, math
from skimage import io
from io import BytesIO
import matplotlib.pyplot as plt
%matplotlib inline

TOKEN = "YOUR TOKEN HERE"

# Function to check the URL and Http request status
def check_URL(reqURL):
    print("URL:", reqURL.url)
    if ((reqURL.status_code == 200)):
        print("Status: ", reqURL.status_code, "OK")
    elif (reqURL.status_code == 404):
        print("Status: ", reqURL.status_code, "Not Found")
    else:
        print("Status: ", reqURL.status_code, "ERROR: Check your parameter!!")

# Function to get scenes from ASNARO-1 satellite at specific latitude and longitude
def get_ASNARO_scene(min_lat, min_lon, max_lat, max_lon):
    url = "https://gisapi.tellusxdp.com/api/v1/asnaro1/scene" \
        + "?min_lat={}&min_lon={}&max_lat={}&max_lon={}".format(min_lat, min_lon, max_lat, max_lon)
    
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + TOKEN
    }
    
    r = requests.get(url, headers=headers)
    
    # Check request URL 
    check_URL(r)

    return r.json()

# Call function to retrieve scenes from ASNARO-1 at specific Latitude and Longitude
scenes = get_ASNARO_scene(20.425278, 122.933611, 45.557222, 153.986389)

# Find the number of scenes
number_scenes = len(scenes)
print ("Number of scenes: ", number_scenes)

# Function to get content from scenes index
def get_scene(_imgIndex, _scenes):
    acquisitionDate = _scenes[_imgIndex]['acquisitionDate']
    cloudCover = _scenes[_imgIndex]['cloudCover']
    entityId = _scenes[_imgIndex]['entityId']
    productId = _scenes[_imgIndex]['productId']
    thumbs_url = _scenes[_imgIndex]['thumbs_url']
    img_thumbs = io.imread(thumbs_url)
    print('imageIndex \t: ', imgIndex)
    print('imageDate \t: ', acquisitionDate)
    print('cloudCover \t: ',cloudCover)
    print('entityId \t: ',entityId)
    print('productId \t: ',productId)
    print('thumbs_url \t: ',thumbs_url)
    
    # Print image from thumbs_url
    io.imshow(img_thumbs)

# Define the first scene index
imgIndex = 0

# Call function to get scene from specific index
if (imgIndex <= number_scenes):
    get_scene(imgIndex, scenes)
    
    #increment imgIndex
    imgIndex = imgIndex + 1
    
# Call function to get scene from specific index
if (imgIndex <= number_scenes):
    get_scene(imgIndex, scenes)
    
    #increment imgIndex
    imgIndex = imgIndex + 1
    
# Call function to get scene from the LAST index
imgIndex = len(scenes)-1 # or, you may set as: imgIndex = -1
if (imgIndex <= number_scenes):
    get_scene(imgIndex, scenes)
    
# Function to get tile coordinate
# Tile: https://maps.gsi.go.jp/development/tileCoordCheck.html#5/35.362/138.731
def get_tile_num(lat_deg, lon_deg, zoom):
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


# Define scene index and zoom
imgIndex = 1
zoom = 10
# Call function to get tile coordinate from specific index
(xtile, ytile) = get_tile_num(scenes[imgIndex]['clat'], scenes[imgIndex]['clon'], zoom)
print(xtile, ytile)

def get_ASNARO_image(scene_id, zoom, xtile, ytile):
    url = " https://gisapi.tellusxdp.com/ASNARO-1/{}/{}/{}/{}.png".format(scene_id, zoom, xtile, ytile)
    headers = {
        "Authorization": "Bearer " + TOKEN
    }
    
    r = requests.get(url, headers=headers)
    
    # Check request URL 
    check_URL(r)
    print(r.content)
    #return io.imread(BytesIO(r.content))


#imgIndex = 0
#imgIndex = -1
#get_scene(imgIndex, scenes)

#print(scene[0]['entityId'])
img = get_ASNARO_image(scenes[-1]['entityId'], zoom, xtile, ytile)

#io.imshow(img)

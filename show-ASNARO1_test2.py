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
    if ((reqURL.status_code == 200)):
        print("URL:", reqURL.url)
        print("Status: ", reqURL.status_code, "OK")
        return True
    elif (reqURL.status_code == 404):
        #print("Status: ", reqURL.status_code, "Not Found")
        return False
    else:
        #print("Status: ", reqURL.status_code, "ERROR: Check your parameter!!")
        return False

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
    if check_URL(r):
        return r.json()

# Function to get content info from scenes index
def get_scene_info(_imgIndex, _scenes):
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
    
# Function to get content from scenes index and display the image
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
    
# Function to get tile coordinate
# Tile: https://maps.gsi.go.jp/development/tileCoordCheck.html#5/35.362/138.731
def get_tile_num(lat_deg, lon_deg, zoom):
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

# Function to get optical image (ASNARO-1) by specifying the point of x, y, z
def get_ASNARO_image(scene_id, zoom, xtile, ytile):
    url = " https://gisapi.tellusxdp.com/ASNARO-1/{}/{}/{}/{}.png".format(scene_id, zoom, xtile, ytile)
    headers = {
        "Authorization": "Bearer " + TOKEN
    }
    
    r = requests.get(url, headers=headers)
    
    # Check request URL 
    if check_URL(r):
        return io.imread(BytesIO(r.content))
    #print(r.content)    
    #return io.imread(BytesIO(r.content))
    
# Call function to retrieve scenes from ASNARO-1 at specific Latitude and Longitude
scenes = get_ASNARO_scene(20.425278, 122.933611, 45.557222, 153.986389)

# Find the number of scenes
number_scenes = len(scenes)
print ("Number of scenes: ", number_scenes)

for zoom in range(10,11):
    for imgIndex in range(0,len(scenes)):
        (xtile, ytile) = get_tile_num(scenes[imgIndex]['clat'], scenes[imgIndex]['clon'], zoom)
        #print("zoom:",zoom,"imgIndex:", imgIndex)
        #print("x:",xtile,"y:", ytile)
        print("index:", imgIndex, "x:",xtile,"y:",ytile,"z:",zoom)
        img = get_ASNARO_image(scenes[imgIndex]['entityId'],zoom,xtile,ytile)
        if img is not None:
            get_scene_info(imgIndex,scenes)
        else:
            print("---- Tellus image is not available ----")

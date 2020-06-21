# Reference link: 
# https://www.tellusxdp.com/ja/howtouse/dev/20200219_000172.html
# How to use the ASNARO1 API from Tellus

import json, requests, time
from skimage import io

TOKEN = "YOUR TOKEN HERE"

# 任意の最小緯度・経度、最大緯度・経度を入力します
# Set your latitute and longitude
min_lat = 32.4440
min_lon = 129.5224
max_lat = 33.4440
max_lon = 130.5224

# URLはサーバーURL+parametersとなります
# Put the URL and parameters
url = "https://gisapi.tellusxdp.com/api/v1/asnaro1/scene" \
  + "?min_lat={}&min_lon={}&max_lat={}&max_lon={}".format(min_lat, min_lon, max_lat, max_lon)

# header情報として、トークンを設定します
# Put your API-token on header
headers = {
  "Authorization": "Bearer " + TOKEN
}

r = requests.get(url, headers=headers)

# Check the URL and Http request status
print("URL:", r.url)
print("Status: ", r.status_code)

# Get all json data from the longitude and latitude we have defined before
print(r.json())

#シーン情報を変数に格納
#Put json information as scenes
scenes = r.json() 

# Find the number of scenes
number_scenes = scenes.__len__()
print ("Number of scenes: ", number_scenes)

# Print information on each scene at specific index
imgIndex = 0
if (imgIndex <= number_scenes):
    acquisitionDate = scenes[imgIndex]['acquisitionDate']
    cloudCover = scenes[imgIndex]['cloudCover']
    entityId = scenes[imgIndex]['entityId']
    productId = scenes[imgIndex]['productId']
    thumbs_url = scenes[imgIndex]['thumbs_url']
    img_thumbs = io.imread(thumbs_url)
    print('imageIndex \t: ', imgIndex)
    print('imageDate \t: ', acquisitionDate)
    print('cloudCover \t: ',cloudCover)
    print('entityId \t: ',entityId)
    print('productId \t: ',productId)
    print('thumbs_url \t: ',thumbs_url)
    
    # Print the image
    io.imshow(img_thumbs)
    
    #increment the imgIndex
    imgIndex = imgIndex + 1
    
# Print information on each scene at specific index
if (imgIndex <= number_scenes):
    acquisitionDate = scenes[imgIndex]['acquisitionDate']
    cloudCover = scenes[imgIndex]['cloudCover']
    entityId = scenes[imgIndex]['entityId']
    productId = scenes[imgIndex]['productId']
    thumbs_url = scenes[imgIndex]['thumbs_url']
    img_thumbs = io.imread(thumbs_url)
    print('imageIndex \t: ', imgIndex)
    print('imageDate \t: ', acquisitionDate)
    print('cloudCover \t: ',cloudCover)
    print('entityId \t: ',entityId)
    print('productId \t: ',productId)
    print('thumbs_url \t: ',thumbs_url)
    
    # Print the image
    io.imshow(img_thumbs)
    
    #increment the imgIndex
    imgIndex = imgIndex + 1
    
# Print information on each scene at specific index
if (imgIndex <= number_scenes):
    acquisitionDate = scenes[imgIndex]['acquisitionDate']
    cloudCover = scenes[imgIndex]['cloudCover']
    entityId = scenes[imgIndex]['entityId']
    productId = scenes[imgIndex]['productId']
    thumbs_url = scenes[imgIndex]['thumbs_url']
    img_thumbs = io.imread(thumbs_url)
    print('imageIndex \t: ', imgIndex)
    print('imageDate \t: ', acquisitionDate)
    print('cloudCover \t: ',cloudCover)
    print('entityId \t: ',entityId)
    print('productId \t: ',productId)
    print('thumbs_url \t: ',thumbs_url)
    
    # Print the image
    io.imshow(img_thumbs)
    
    #increment the imgIndex
    imgIndex = imgIndex + 1

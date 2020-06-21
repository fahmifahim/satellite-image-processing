# Reference link: 
# https://www.tellusxdp.com/ja/howtouse/dev/20200219_000172.html

import json, requests, time
from skimage import io

TOKEN = "YOUR TOKEN HERE"

# 任意の最小緯度・経度、最大緯度・経度を入力します
min_lat = 32.4440
min_lon = 129.5224
max_lat = 33.4440
max_lon = 130.5224

# URLはサーバーURL+parametersとなります
url = "https://gisapi.tellusxdp.com/api/v1/asnaro1/scene" \
  + "?min_lat={}&min_lon={}&max_lat={}&max_lon={}".format(min_lat, min_lon, max_lat, max_lon)

# header情報として、トークンを設定します
headers = {
  "Authorization": "Bearer " + TOKEN
}

r = requests.get(url, headers=headers)

# Check the URL and Http request status
print("URL:", r.url)
print("Status: ", r.status_code)

print(r.json())

#シーン情報を変数に格納
scenes = r.json() 

#scenesに含まれる最後のメタ情報からサムネイル画像URLを取得
img1 = scenes[-1]['thumbs_url'] 

img_thumbs1 = io.imread(scenes[-1]['thumbs_url'])
io.imshow(img_thumbs1)

img_thumbs = io.imread(scenes[1]['thumbs_url'])
io.imshow(img_thumbs)

img_thumbs = io.imread(scenes[2]['thumbs_url'])
io.imshow(img_thumbs)

img_thumbs = io.imread(scenes[3]['thumbs_url'])
io.imshow(img_thumbs)

img_thumbs = io.imread(scenes[4]['thumbs_url'])
io.imshow(img_thumbs)

img_thumbs = io.imread(scenes[5]['thumbs_url'])
io.imshow(img_thumbs)

img_thumbs = io.imread(scenes[0]['thumbs_url'])
io.imshow(img_thumbs)

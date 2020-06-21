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

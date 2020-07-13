# Install below packages in advance
#!pip install sentinelsat
#!pip install rasterio
#!apt install gdal-bin python-gdal python3-gdal 
#!apt install python3-rtree 
#!pip install git+git://github.com/geopandas/geopandas.git
#!pip install descartes 
#!pip install shapely
#!pip install six
#!pip install pyproj
#!pip install descartes
#!pip install geopandas
#!pip install folium

import os
import numpy as np

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt 
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from shapely.geometry import MultiPolygon, Polygon
import rasterio as rio
from rasterio.plot import show
import rasterio.mask
import fiona
import folium 

from IPython.display import HTML
HTML(r'<iframe width="960" height="480" src="https://www.keene.edu/campus/maps/tool/" frameborder="0"></iframe>')

# Define the area for 国会議事堂
AREA = [
    [
        -220.2588844,
        35.678773
    ],
    [
        -220.2582836,
        35.6733346
    ],
    [
        -220.2527905,
        35.6738575
    ],
    [
        -220.254271,
        35.679017
    ],
    [
        -220.2588844,
        35.678773
    ]
]

for i in range(len(AREA)):
    AREA[i][0] = AREA[i][0] +360

m=Polygon([AREA]) 

#ファイル名を定義. 好きな名称に設定してください. 
object_name = 'Tokyo_HouseOfParliament'


with open(str(object_name) +'.geojson', 'w') as f:
    json.dump(m, f)
footprint_geojson = geojson_to_wkt(read_geojson(str(object_name) +'.geojson'))

user = 'YOUR=USER' 
password = 'PASSWORD' 
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

m = folium.Map([(AREA[0][1]+AREA[len(AREA)-1][1])/2,(AREA[0][0]+AREA[len(AREA)-1][0])/2], zoom_start=10)

folium.GeoJson(str(object_name) +'.geojson').add_to(m)
m

#光学画像であるSentinel-2の画像を取得するため、既に指定している「場所」の情報以外である以下4つ：
#・対象とする衛星
#・期間
#・データの処理レベル
#・被雲率
products = api.query(footprint_geojson,
                     date = ('20200601', '20200701'), #取得希望期間の入力
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0,100)) #被雲率（0％〜100％）

len(products)

products_gdf = api.to_geodataframe(products)
products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
products_gdf_sorted

products_gdf_sorted.head()

uuid = products_gdf_sorted.iloc[0]["uuid"]
product_title = products_gdf_sorted.iloc[0]["title"]
api.download(uuid)

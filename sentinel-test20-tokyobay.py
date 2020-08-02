import os
import numpy as np

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt 
from shapely.geometry import MultiPolygon, Polygon
from rasterio.plot import show
from geojson import Polygon
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import rasterio as rio
import rasterio.mask
import fiona
import folium
import zipfile


#関心領域のポリゴン情報の取得
from IPython.display import HTML
HTML(r'<iframe width="960" height="480" src="https://www.keene.edu/campus/maps/tool/" frameborder="0"></iframe>')

#上記にて取得した地理情報をコピペする
AREA = [
          [
            -220.291841,
            35.6593884
          ],
          [
            -220.2932143,
            35.4817801
          ],
          [
            -220.1380324,
            35.4817801
          ],
          [
            -220.1421523,
            35.6493456
          ],
          [
            -220.291841,
            35.6593884
          ]
        ]

print(AREA)
print(len(AREA))
print(AREA[0])
print(AREA[0][0])


# Convert coordinate to 360degree format
for i in range(len(AREA)):
    AREA[i][0] = AREA[i][0] +360

# Check the result before the conversion
print(AREA)
print(len(AREA))
print(AREA[0])
print(AREA[0][0])

# Convert coordinate to Polygon format
m=Polygon([AREA]) 
print(m)

#ファイル名を定義. 好きな名称に設定してください. 
object_name = 'Tokyo_Bay'

# Convert the Polygon data to GeoJSON format
with open(str(object_name) +'.geojson', 'w') as f:
    json.dump(m, f)

# Convert a GeoJSON object to Well-Known Text. Intended for use with OpenSearch queries.
footprint_geojson = geojson_to_wkt(read_geojson(str(object_name) +'.geojson'))
print(footprint_geojson)

# Sentinel API credentials
user = 'username' 
password = 'password' 
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


# Create a base map, simply by passing the starting coordinates to Folium
# In this case get the coordinate from the first and last x,y divided by 2
x_map = (AREA[0][1]+AREA[len(AREA)-1][1])/2
y_map = (AREA[0][0]+AREA[len(AREA)-1][0])/2
xyzoom_start = 11

m = folium.Map([x_map, y_map], zoom_start=xyzoom_start)
#m = folium.Map([(AREA[0][1]+AREA[len(AREA)-1][1])/2,(AREA[0][0]+AREA[len(AREA)-1][0])/2], zoom_start=zoom_start)

# Add the GeoJSON data (coordinate info) to folium
folium.GeoJson(str(object_name) +'.geojson').add_to(m)

# Display the Folium map on OpenStreetMap
m

# Reference https://sentinelsat.readthedocs.io/en/stable/api.html?highlight=api.query#quickstart

#取得希望期間の入力と被雲率
start_date = '20200601'
end_date = '20200801'
cloudcover_percentage = (0,100) # 被雲率 0〜100%

products = api.query(footprint_geojson,
                     date = (start_date, end_date), 
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = cloudcover_percentage) 

print("Number of scenes = ", len(products))

# Return the products from a query response as a GeoPandas GeoDataFrame with the values in their appropriate Python types.
products_gdf = api.to_geodataframe(products)

# Sort values from the least percentage of cloudcover scenes
# Sort reference: https://sentinelsat.readthedocs.io/en/stable/api.html?highlight=to_geodataframe(products)#sorting-filtering
products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])

# Display the sorted data
products_gdf_sorted


# Display first 5 data (head function)
products_gdf_sorted.head()


# Download the first sorted scene (smallest cloud percentage)
print(products_gdf_sorted.iloc[0])
uuid = products_gdf_sorted.iloc[0]["uuid"]
product_title = products_gdf_sorted.iloc[0]["title"]


# Download image from the first sorted query
api.download(uuid)

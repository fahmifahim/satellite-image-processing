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

#関心領域のポリゴン情報の取得
from IPython.display import HTML
HTML(r'<iframe width="960" height="480" src="https://www.keene.edu/campus/maps/tool/" frameborder="0"></iframe>')

#上記にて取得した地理情報をコピペする
AREA =  [
      [
        150.3934479,
        -34.2354585
      ],
      [
        150.3925323,
        -34.3063876
      ],
      [
        150.5703735,
        -34.3064821
      ],
      [
        150.5707169,
        -34.23508
      ],
      [
        150.3934479,
        -34.2354585
      ]
    ]

print(AREA)

# Right and Left clock coordinate
for i in range(len(AREA)):
    if AREA[i][0] >= 0:
        AREA[i][0] = AREA[i][0]%360
    else:
        AREA[i][0] = -(abs(AREA[i][0])%360) + 360

print(AREA)


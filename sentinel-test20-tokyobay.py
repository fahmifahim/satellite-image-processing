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

# Extract the downloaded zip files
file_name = str(product_title) +'.zip'

with zipfile.ZipFile(file_name) as zf:
 zf.extractall()

 # Path to image files
path = str(product_title) + '.SAFE/GRANULE'
files = os.listdir(path)
print("path = ", path)
print("files = ", files)

pathA = str(product_title) + '.SAFE/GRANULE/' + str(files[0])
files2 = os.listdir(pathA)
print("pathA = ", pathA)
print("files2 = ", files2)

pathB = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m'
files3 = os.listdir(pathB)
print("pathB = ", pathB)
print("files3 = ", files3)

# Data tree
#S2B_MSIL2A_20200726T012659_N0214_R074_T54SUE_20200726T042423.SAFE
#├── AUX_DATA
#├── DATASTRIP
#│   └── DS_EPAE_20200726T042423_S20200726T012657
#│       ├── MTD_DS.xml
#│       └── QI_DATA
#│           ├── FORMAT_CORRECTNESS.xml
#│           ├── GENERAL_QUALITY.xml
#│           ├── GEOMETRIC_QUALITY.xml
#│           ├── RADIOMETRIC_QUALITY.xml
#│           └── SENSOR_QUALITY.xml
#├── GRANULE
#│   └── L2A_T54SUE_A017689_20200726T012657
#│       ├── AUX_DATA
#│       │   └── AUX_ECMWFT
#│       ├── IMG_DATA
#│       │   ├── R10m
#│       │   │   ├── T54SUE_20200726T012659_AOT_10m.jp2
#│       │   │   ├── T54SUE_20200726T012659_B02_10m.jp2  # Band2(Red)
#│       │   │   ├── T54SUE_20200726T012659_B03_10m.jp2  # Band3(Green)
#│       │   │   ├── T54SUE_20200726T012659_B04_10m.jp2  # Band4(Blue)
#│       │   │   ├── T54SUE_20200726T012659_B08_10m.jp2
#│       │   │   ├── T54SUE_20200726T012659_TCI_10m.jp2
#│       │   │   └── T54SUE_20200726T012659_WVP_10m.jp2
#│       │   ├── R20m
#│       │   │   ├── T54SUE_20200726T012659_AOT_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_B02_20m.jp2  # Band2(Red)
#│       │   │   ├── T54SUE_20200726T012659_B03_20m.jp2  # Band3(Green)
#│       │   │   ├── T54SUE_20200726T012659_B04_20m.jp2  # Band4(Blue)
#│       │   │   ├── T54SUE_20200726T012659_B05_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_B06_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_B07_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_B11_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_B12_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_B8A_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_SCL_20m.jp2
#│       │   │   ├── T54SUE_20200726T012659_TCI_20m.jp2
#│       │   │   └── T54SUE_20200726T012659_WVP_20m.jp2
#│       │   └── R60m
#│       │       ├── T54SUE_20200726T012659_AOT_60m.jp2
#│       │       ├── T54SUE_20200726T012659_B01_60m.jp2
#│       │       ├── T54SUE_20200726T012659_B02_60m.jp2  # Band2(Red)
#│       │       ├── T54SUE_20200726T012659_B03_60m.jp2  # Band3(Green)
#│       │       ├── T54SUE_20200726T012659_B04_60m.jp2  # Band4(Blue)
#│       │       ├── T54SUE_20200726T012659_B05_60m.jp2
#│       │       ├── T54SUE_20200726T012659_B06_60m.jp2
#│       │       ├── T54SUE_20200726T012659_B07_60m.jp2
#│       │       ├── T54SUE_20200726T012659_B09_60m.jp2
#│       │       ├── T54SUE_20200726T012659_B11_60m.jp2
#│       │       └── T54SUE_20200726T012659_WVP_60m.jp2
#│       ├── MTD_TL.xml
#│       └── QI_DATA
#│
#├── HTML
#│   ├── UserProduct_index.html
#│   ├── UserProduct_index.xsl
#│   ├── banner_1.png
#│   ├── banner_2.png
#│   ├── banner_3.png
#│   └── star_bg.jpg
#├── INSPIRE.xml
#├── MTD_MSIL2A.xml
#├── manifest.safe
#└── rep_info
#    ├── S2_PDI_Level-2A_Datastrip_Metadata.xsd
#    ├── S2_PDI_Level-2A_Tile_Metadata.xsd
#    └── S2_User_Product_Level-2A_Metadata.xsd


# Open Bands 4(Blue), 3(Green) and 2(Red) with Rasterio(rio)
# We are using the 10m resolutions
path_b2 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B02_10m.jp2')
path_b3 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B03_10m.jp2')
path_b4 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B04_10m.jp2')

b4 = rio.open(path_b4)
b3 = rio.open(path_b3)
b2 = rio.open(path_b2)


# Observe the Band 4 CRS (Coordinate Reference System)
b4.count, b4.width, b4.height

# Reference https://rasterio.readthedocs.io/en/latest/api/rasterio.crs.html#module-rasterio.crs
b4.crs

# EPSGの326544というのは、地図投影する際によく利用される、WGS84のUTM座標系のことを表します。

fig, ax = plt.subplots(1, figsize=(20, 20))
show(b4, ax=ax)
plt.show()

# バンドを合成してTrue ColorのRGB画像を表示
# Sentinel-2の１シーン画像として .tiff ファイルが出力される
with rio.open(str(object_name) +'.tiff','w',driver='Gtiff', width=b4.width, height=b4.height, 
              count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0]) as rgb:
    rgb.write(b2.read(1),3) 
    rgb.write(b3.read(1),2) 
    rgb.write(b4.read(1),1) 
    rgb.close()

RGB_tokyo =rio.open(str(object_name) +'.tiff')
RGB_tokyo.crs

nReserve_geo = gpd.read_file(str(object_name) +'.geojson')
epsg = b4.crs

# 関心領域のみを抽出して、表示する
# Since this RGB image is large and huge you save both computing power and time to clip and use only the area of interest. 
# We will clip the Natural reserve area from the RGB image.
nReserve_proj = nReserve_geo.to_crs({'init': epsg})

with rio.open(str(object_name) +'.tiff') as src:
    out_image, out_transform = rio.mask.mask(src, nReserve_proj.geometry,crop=True)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})
    
with rasterio.open('Masked_' +str(object_name) +'.tif', "w", **out_meta) as dest:
    dest.write(out_image)

msk = rio.open(r'Masked_' +str(object_name) +'.tif')
fig, ax = plt.subplots(1, figsize=(18, 18))
show(msk.read([1,2,3]))
plt.show
# The result will be displayed in 16 bit image
# You need to adjust the histogram to make it visible by human (or, convert it to jpeg format)

# ローカル環境でも表示しやすいjpg形式にファイルを変換してみましょう。
# jpgに変換すると勝手にヒストグラムが調整される…？

from osgeo import gdal

scale = '-scale 0 250 0 30'
options_list = [
    '-ot Byte',
    '-of JPEG',
    scale
] 
options_string = " ".join(options_list)

gdal.Translate('Masked_' +str(object_name) +'.jpg',
               'Masked_' +str(object_name) +'.tif',
               options=options_string)

from PIL import Image
im = Image.open('Masked_' +str(object_name) +'.jpg')
im

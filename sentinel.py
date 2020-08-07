# IMPORTANT: Make sure you install below packages in advance
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
from shapely.geometry import MultiPolygon, Polygon
from rasterio.plot import show
from geojson import Polygon
from osgeo import gdal
from PIL import Image, ImageDraw, ImageFont
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import shutil
import glob

import rasterio as rio
import rasterio.mask
import fiona
import folium
import zipfile


#Generate coordinate of Area of Interest by using tools from Keene University below
#from IPython.display import HTML
#HTML(r'<iframe width="960" height="480" src="https://www.keene.edu/campus/maps/tool/" frameborder="0"></iframe>')

# Sentinel API credentials
user = 'username' 
password = 'password' 
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


def sentinel2_hello():
    print("Hello from Sentinel2")
    

# Convert the Polygon data to GeoJSON format
def Sentinel2_convert_polygon_to_json(object_name, polygon_object):
    print("Converting polygon to GeoJSON...")
    with open(object_name +'.geojson', 'w') as f:
        json.dump(polygon_object, f)
        print(object_name +".geojson created")

## Get Sentinel satellite scene
def Sentinel2_get_sorted_data(i):
    products = api.query(footprint_geojson,
                     date = (Begin_date, End_date1), #Desired date for the beginning and ending time of Sentinel-2 image
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0,100)) 
    
    products_gdf = api.to_geodataframe(products)
    
    
    #Sort the value of cloud coverage percentage from the small one
    products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
    title = products_gdf_sorted.iloc[i]["title"]
    print(str(title))
    
    uuid = products_gdf_sorted.iloc[i]["uuid"]
    product_title = products_gdf_sorted.iloc[i]["title"]
    
    #Check the date of the first element of the sorted scenes
    date = products_gdf_sorted.iloc[i]["ingestiondate"].strftime('%Y-%m-%d')
    print(date)
    
    #Download Sentinel-2 data 
    api.download(uuid)
    file_name = str(product_title) +'.zip'
    print("file_name = ", file_name)
    
    
    #Extract downloaded Sentinel-2 data
    print("Extracting zip file...")
    with zipfile.ZipFile(file_name) as zf:
        zf.extractall()
    
    #Get image's folder path 
    path = str(product_title) + '.SAFE/GRANULE'
    files = os.listdir(path)
    pathA = str(product_title) + '.SAFE/GRANULE/' + str(files[0])
    files2 = os.listdir(pathA)
    pathB = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m'
    files3 = os.listdir(pathB)
    
    
    print("Resolution 10m files identification...")
    path_b2 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B02_10m.jp2')
    path_b3 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B03_10m.jp2')
    path_b4 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B04_10m.jp2')
    
    #Open Band4(Blue), 3(Green) and 2(Red)
    b4 = rio.open(path_b4)
    b3 = rio.open(path_b3)
    b2 = rio.open(path_b2)
    
    #RGB color compose (output file as GeoTiff: public domain metadata standard which allows georeferencing information to be embedded within a TIFF file) 
    print("RGB Color composing...")
    with rio.open(str(object_name) +'.tiff','w',driver='Gtiff', width=b4.width, height=b4.height, 
              count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0]) as rgb:
        rgb.write(b4.read(1),1) 
        rgb.write(b3.read(1),2) 
        rgb.write(b2.read(1),3) 
        rgb.close()
    
    #Read polygon from .geojson
    nReserve_geo = gpd.read_file(str(object_name) +'.geojson')
    
    # Reference https://rasterio.readthedocs.io/en/latest/api/rasterio.crs.html#module-rasterio.crs
    # EPSGの326544というのは、地図投影する際によく利用される、WGS84のUTM座標系のことを表します。
    epsg = b4.crs
    
    # Since this RGB image is large and huge you save both computing power and time to clip and use only the area of interest. 
    # We will clip the Natural reserve area from the RGB image.
    nReserve_proj = nReserve_geo.to_crs({'init': str(epsg)})
    
    #Create directory for temporary Masked Tiff
    print("Creating directory Image_tiff...")
    os.makedirs('./Image_tiff', exist_ok=True)

    #Extract image for Area of Interest from the composed color image
    print("Calculating area of interest...")
    with rio.open(str(object_name) +'.tiff') as src:
        out_image, out_transform = rio.mask.mask(src, nReserve_proj.geometry,crop=True)
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
    
    with rasterio.open('./Image_tiff/' +'Masked_' +str(object_name) +'.tif', "w", **out_meta) as dest:
        dest.write(out_image)
    
    #jpeg processing from the extracted images
    scale = '-scale 0 250 0 30'
    options_list = [
        '-ot Byte',
        '-of JPEG',
        scale
    ] 
    
    options_string = " ".join(options_list)
    
    #Create directory for jpeg processed image 
    print("Creating Image_jpeg...")
    os.makedirs('./Image_jpeg_'+str(object_name), exist_ok=True)
    
    #Save jpeg image
    #https://pypi.org/project/GDAL/
    #GDAL Geospatial Data Abstraction Library
    gdal.Translate('./Image_jpeg_'+str(object_name) +'/' + str(Begin_date) + 'Masked_' +str(object_name) +'.jpg',
                   './Image_tiff/Masked_' +str(object_name) +'.tif',
                   options=options_string)
    
    
    #Print the date on the image
    img = Image.open('./Image_jpeg_'+str(object_name) +'/' + str(Begin_date) + 'Masked_' +str(object_name) +'.jpg')
    #print(img.size)
    #print(img.size[0])
    x = img.size[0]/100 #x coordinate for the print position
    y = img.size[1]/100 #y coordinate for the print position
    fs = img.size[0]/50 #font size
    fs1 = int(fs)
    #print(fs1)
    #print(type(fs1))
    obj_draw = ImageDraw.Draw(img)
    obj_font = ImageFont.truetype(fontfile, fs1)
    obj_draw.text((x, y), str(date), fill=(255, 255, 255), font=obj_font)
    obj_draw.text((img.size[0]/2, img.size[1]-y - img.size[1]/20 ), 'produced from ESA remote sensing data', fill=(255, 255, 255), font=obj_font)
    

    img.save('./Image_jpeg_'+str(object_name) +'/' + str(Begin_date) + 'Masked_' +str(object_name) +'.jpg')
    
    #Remove downloaded files
    print("Removing files...")
    shutil.rmtree( str(product_title) + '.SAFE')
    os.remove(str(product_title) +'.zip')
    
    print("--DONE--")
    return

def Sentinel2_get():
    products = api.query(footprint_geojson,
                     date = (Begin_date, End_date), #取得希望期間の入力
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A', #Leve-1C
                     cloudcoverpercentage = (0,100)) #被雲率（０％〜５０％）
    
    products_gdf = api.to_geodataframe(products)
    products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
    
    #同一シーンの画像を取得するため，placenumberを固定する．
    products_gdf_sorted = products_gdf_sorted[products_gdf_sorted["title"].str.contains(placenumber)]
    title = products_gdf_sorted.iloc[0]["title"]
    print(str(title))
    
    uuid = products_gdf_sorted.iloc[0]["uuid"]
    product_title = products_gdf_sorted.iloc[0]["title"]
    
  
    date = products_gdf_sorted.iloc[0]["ingestiondate"].strftime('%Y-%m-%d')
    print(date)
    
    api.download(uuid)
    file_name = str(product_title) +'.zip'
    print("file_name = ", file_name)
    
    print("Extracting zip file...")
    with zipfile.ZipFile(file_name) as zf:
        zf.extractall()
    
    path = str(product_title) + '.SAFE/GRANULE'
    files = os.listdir(path)
    pathA = str(product_title) + '.SAFE/GRANULE/' + str(files[0])
    files2 = os.listdir(pathA)
    pathB = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m'
    files3 = os.listdir(pathB)
    
    print("Resolution 10m files identification...")
    path_b2 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B02_10m.jp2')
    path_b3 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B03_10m.jp2')
    path_b4 = str(product_title) + '.SAFE/GRANULE/' + str(files[0]) +'/' + str(files2[1]) +'/R10m/' +str(files3[0][0:23] +'B04_10m.jp2')
    
    b4 = rio.open(path_b4)
    b3 = rio.open(path_b3)
    b2 = rio.open(path_b2)
    
    print("RGB Color composing...")
    with rio.open(str(object_name) +'.tiff','w',driver='Gtiff', width=b4.width, height=b4.height, 
              count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0]) as rgb:
        rgb.write(b4.read(1),1) 
        rgb.write(b3.read(1),2) 
        rgb.write(b2.read(1),3) 
        rgb.close()
    
    print("Creating directory Image_tiff...")
    os.makedirs('./Image_tiff', exist_ok=True)
    
    nReserve_geo = gpd.read_file(str(object_name) +'.geojson')
    epsg = b4.crs
    
    nReserve_proj = nReserve_geo.to_crs({'init': str(epsg)})

    print("Calculating area of interest...")
    with rio.open(str(object_name) +'.tiff') as src:
        out_image, out_transform = rio.mask.mask(src, nReserve_proj.geometry,crop=True)
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
    
    with rasterio.open('./Image_tiff/' +'Masked_' +str(object_name) +'.tif', "w", **out_meta) as dest:
        dest.write(out_image)
    
    from osgeo import gdal

    scale = '-scale 0 250 0 30'
    options_list = [
        '-ot Byte',
        '-of JPEG',
        scale
    ] 
    options_string = " ".join(options_list)
    
    print("Creating Image_jpeg...")
    os.makedirs('./Image_jpeg_'+str(object_name), exist_ok=True)

    gdal.Translate('./Image_jpeg_'+str(object_name) +'/' + str(Begin_date) + 'Masked_' +str(object_name) +'.jpg',
                   './Image_tiff/Masked_' +str(object_name) +'.tif',
                   options=options_string)
    
    #画像への撮像日の記載
    img = Image.open('./Image_jpeg_'+str(object_name) +'/' + str(Begin_date) + 'Masked_' +str(object_name) +'.jpg')

    #print(img.size)
    #print(img.size[0])
    x = img.size[0]/100 #日付の記載位置の設定
    y = img.size[1]/100 #日付の記載位置の設定
    fs = img.size[0]/50 #日付のフォントサイズの設定
    fs1 = int(fs)
    #print(fs1)
    #print(type(fs1))
    obj_draw = ImageDraw.Draw(img)
    obj_font = ImageFont.truetype(fontfile, fs1)
    obj_draw.text((x, y), str(date), fill=(255, 255, 255), font=obj_font)
    obj_draw.text((img.size[0]/2, img.size[1]-y - img.size[1]/20 ), 'produced from ESA remote sensing data', fill=(255, 255, 255), font=obj_font)
    img.save('./Image_jpeg_'+str(object_name) +'/' + str(Begin_date) + 'Masked_' +str(object_name) +'.jpg')
        
    print("Removing files...")
    shutil.rmtree( str(product_title) + '.SAFE')
    os.remove(str(product_title) +'.zip')
    
    print("--DONE--")
    return

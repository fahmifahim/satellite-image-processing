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



def Sentinel2_get_init(i):
    products = api.query(footprint_geojson,
                     date = (Begin_date, End_date1), #画像取得月の画像取得
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A', #Leve-1C
                     cloudcoverpercentage = (0,100)) #被雲率（0%〜50%）
    
    products_gdf = api.to_geodataframe(products)
    
    #画像取得月の被雲率の小さい画像からソートする．
    products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
    title = products_gdf_sorted.iloc[i]["title"]
    print(str(title))
    
    uuid = products_gdf_sorted.iloc[i]["uuid"]
    product_title = products_gdf_sorted.iloc[i]["title"]
    
    #画像の観測日を確認．
    date = products_gdf_sorted.iloc[i]["ingestiondate"].strftime('%Y-%m-%d')
    print(date)
    
    #Sentinel-2 data download
    api.download(uuid)
    file_name = str(product_title) +'.zip'
    print("file_name = ", file_name)
    
    
    #ダウロードファイルの解凍．
    print("Extracting zip file...")
    with zipfile.ZipFile(file_name) as zf:
        zf.extractall()
    
    #フォルダの画像ファイルのアドレスを取得．
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
    
    # Band４，３，２をR,G,Bとして開く．
    b4 = rio.open(path_b4)
    b3 = rio.open(path_b3)
    b2 = rio.open(path_b2)
    
    #RGBカラー合成（GeoTiffファイルの出力）
    print("RGB Color composing...")
    with rio.open(str(object_name) +'.tiff','w',driver='Gtiff', width=b4.width, height=b4.height, 
              count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0]) as rgb:
        rgb.write(b4.read(1),1) 
        rgb.write(b3.read(1),2) 
        rgb.write(b2.read(1),3) 
        rgb.close()
    
    #ポリゴン情報の取得．
    nReserve_geo = gpd.read_file(str(object_name) +'.geojson')
    
    #取得画像のEPSGを取得
    epsg = b4.crs
    
    nReserve_proj = nReserve_geo.to_crs({'init': str(epsg)})
    
    #マスクTiffファイルの一時置き場
    print("Creating directory Image_tiff...")
    os.makedirs('./Image_tiff', exist_ok=True)

    #カラー合成画像より関心域を抽出．
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
    
    #抽出画像のjpeg処理．
    scale = '-scale 0 250 0 30'
    options_list = [
        '-ot Byte',
        '-of JPEG',
        scale
    ] 
    
    options_string = " ".join(options_list)
    
    #ディレクトリの作成 
    print("Creating Image_jpeg...")
    os.makedirs('./Image_jpeg_'+str(object_name), exist_ok=True)
    
    #jpeg画像の保存．
    gdal.Translate('./Image_jpeg_'+str(object_name) +'/' + str(Begin_date) + 'Masked_' +str(object_name) +'.jpg',
                   './Image_tiff/Masked_' +str(object_name) +'.tif',
                   options=options_string)
    
    #画像への撮像日を記載
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
    
    #大容量のダウンロードファイル，および解凍フォルダの削除
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

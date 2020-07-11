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

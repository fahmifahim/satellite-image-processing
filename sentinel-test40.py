from sentinel2 import *

# Get notebookname
notebookbasename = os.path.basename(notebook_path())
notebookname = os.path.splitext(notebookbasename)[0]
print("JupyterNotebook name : ", notebookname)


# FONT preparation setting. This font will be printed on each image
# 1. Download the font file from https://osdn.net/dl/mplus-fonts/mplus-TESTFLIGHT-063a.tar.xz
# 2. Execute thise command on your environment: wget https://osdn.net/dl/mplus-fonts/mplus-TESTFLIGHT-063a.tar.xz
# 3. Check the downloaded file: ls -l mplus-TESTFLIGHT-063a.tar.xz
# 4. -rw-r--r-- 1 jovyan users 10371708 Apr 23  2019 mplus-TESTFLIGHT-063a.tar.xz
# 5. Put the downloaded file to the same directory as your JupyterNotebook file

cwd = os.getcwd()
suffix = '.ttf'
base_filename = 'mplus-1c-bold'
fontfile = os.path.join(cwd,'mplus-TESTFLIGHT-063a',base_filename + suffix)

# Extract the font file. You may skip the process if it already there
if os.path.isfile(fontfile):
    print("Font file exist : " + fontfile)
else: 
    print("Extracting font file...")
    
    if os.path.isfile("mplus-TESTFLIGHT-063a.tar.xz"):
        !xz -dc mplus-TESTFLIGHT-*.tar.xz | tar xf -
    else:
        print("Font file extraction failed!")
        
    print("Font file extracted")
    if os.path.isfile(fontfile):
        print(fontfile)

#Determine your Area of Interest by using the 
#IMPORTANT: It is currently commented out. Use Polyline Tool from Keene University to find out the area of interest
#from IPython.display import HTML
#HTML(r'<iframe width="960" height="480" src="https://www.keene.edu/campus/maps/tool/" frameborder="0"></iframe>')

#Copy paste the area of interest from the Polyline Tool Keene University 
AREA = [ # Write your area here: Tokyo Bay
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

#Set the Resolution to display. Choose between 10, 20, or 60
resolution = "60"
print("Resolution to retrieve from Sentinel-2 = ", resolution)


# Convert coordinate to 360degree format
for i in range(len(AREA)):
    AREA[i][0] = AREA[i][0] +360

# Convert coordinate to Polygon format
m=Polygon([AREA])

#Set the object name for the area of interest
object_name = str(notebookname)

# Convert the Polygon data to GeoJSON format
Sentinel2_convert_polygon_to_json(object_name, m)

# Convert a GeoJSON object to Well-Known Text. Intended for use with OpenSearch queries.
footprint_geojson = geojson_to_wkt(read_geojson(object_name +'.geojson'))
print(footprint_geojson)


#Get the Sentinel-2 L2A products from the specified starting date
#Specify your desired starting date below
start_date = '20190401'
end_date = start_date[:6] +'28'
#We define the last date each month as 28, considering end of February only 28


#Define the index. Set as 0 if you want to get the first index
index = 0
Sentinel2_get_sorted_data(index, fontfile, object_name, footprint_geojson, start_date, end_date, resolution)

# Show the captured Sentinel2 image
im = Image.open('./Image_jpeg_' + object_name +'/'+ str(start_date) +'Masked_'+ object_name +'.jpg')
print("Showing image...")
print(im)
im

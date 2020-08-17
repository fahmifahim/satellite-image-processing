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
from IPython.display import HTML
HTML(r'<iframe width="960" height="480" src="https://www.keene.edu/campus/maps/tool/" frameborder="0"></iframe>')

#Copy paste the area of interest from the Polyline Tool Keene University 
#Area name = Sabang
AREA = [
          [
            -264.8015785,
            5.9169222
          ],
          [
            -264.7330856,
            5.7640829
          ],
          [
            -264.5839119,
            5.7676695
          ],
          [
            -264.6221924,
            5.9191419
          ],
          [
            -264.8015785,
            5.9169222
          ]
        ]

#Set the Resolution to display. Choose between 10, 20, or 60
resolution = "10"
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

# Create a base map, simply by passing the starting coordinates to Folium
# In this case get the coordinate from the first and last x,y divided by 2
x_map = (AREA[0][1]+AREA[len(AREA)-1][1])/2
y_map = (AREA[0][0]+AREA[len(AREA)-1][0])/2
xyzoom_start = 11

m = folium.Map([x_map, y_map], zoom_start=xyzoom_start)

# Add the GeoJSON data (coordinate info) to folium
folium.GeoJson(str(object_name) +'.geojson').add_to(m)

# Display the Folium map on OpenStreetMap
m

#Get the Sentinel-2 L2A products from the specified starting date
#Specify your desired starting and ending date
start_date = '20190801'
end_date = '20200831'

#Define the index. Set as 0 if you want to get the first index
index = 0

#Count the number of months from different years
num_months = int(end_date[2:4]) - int(start_date[2:4])
num_months = num_months*12 + int(end_date[4:6]) - int(start_date[4:6])

#Get one scene each month, and create the jpeg image
for i in range(num_months):
    if i < 1:
        m = int(start_date[4:6])
    else:
        m = int(start_date[4:6]) +1

    if m <10:
        start_date = start_date[:4] +'0'+ str(m) + start_date[6:]
    elif m <13:
        start_date = start_date[:4] + str(m) + start_date[6:]
    else:
        y = int(start_date[2:4]) +1
        start_date = start_date[:2] + str(y) + '01' + start_date[6:]
        
    end_date = start_date[:6] +'28'
    # Call the Sentinel function
    Sentinel2_get_sorted_data(index, fontfile, object_name, footprint_geojson, start_date, end_date, resolution)


# Create GIF animation from jpeg images. Amimation created in the order of time
images =[]

files = sorted(glob.glob('./Image_jpeg_'+object_name +'/*.jpg'))
images = list(map(lambda file: Image.open(file), files))

images[0].save('./Image_jpeg_'+object_name +'/' + object_name + '.gif', save_all=True, append_images=images[1:], duration=1500, loop=0)

# Show GIF image
gif_file = './Image_jpeg_'+object_name +'/' + object_name + '.gif'
print("Created GIF file = ", gif_file)

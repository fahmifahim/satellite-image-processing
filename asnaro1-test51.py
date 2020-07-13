from asnaro import *

# Tokyo station: 35.6812362,139.7649361
a_scenes=get_ASNARO_scene(20.425278, 122.933611, 45.557222, 153.986389)

a_scenes_length = len(a_scenes)
print("Scenes length : ", a_scenes_length)

#観察したい地域の緯度経度を指定する latitude & longitude 
min_lat = 20.425278
min_lon = 122.933611
max_lat = 45.557222
max_lon = 153.986389
asnaro_scene = get_ASNARO_scene(min_lat, min_lon, max_lat, max_lon)
#Filter scene in order
asnaro_scenes = filter_by_date(asnaro_scene, 
                               datetime(2014, 12, 7, tzinfo=timezone.utc),
                               datetime(2019, 12, 31, tzinfo=timezone.utc))

print("Asnaro Scenes: ", len(asnaro_scenes))

#Specify your observation areas here : 
observation_areas = [
    {
        "name":"東京駅",
        "lat": 35.6812362,
        "lon": 139.7649361
    },
    {
        "name":"新宿駅",
        "lat": 35.689607,
        "lon": 139.700571
    },
    {
        "name":"国会議事堂",
        "lat": 35.675888,
        "lon": 139.7426693
    }
]

#Classify scenes by calculating distances and sort the acquisitionDate
#Calculate the difference between lat&lot of the observation areas and the firstly defined area 
classified_scenes = classify(observation_areas, asnaro_scenes)

tokyostation_scenes = classified_scenes[0]
shinjukustation_scenes = classified_scenes[1]
kokkai_scenes = classified_scenes[2]
print("東京駅-ASNARO: ",len(tokyostation_scenes))
print("新宿駅-ASNARO:",len(shinjukustation_scenes))
print("国会議事堂-ASNARO：",len(kokkai_scenes))

# 以下東京駅表示にエラー。。。

# Refer the Tile info from the below URL to get the specific zoom, xtile and ytile
# https://maps.gsi.go.jp/development/tileCoordCheck.html#18/35.68131/139.76678

#zoom=17
#xtile=116419
#ytile=51613
#tokyostation_image = get_ASNARO_image(tokyostation_scenes[0]["entityId"], zoom, xtile, ytile)
#print(tokyostation_image)
#io.imshow(tokyostation_image)
#plt.imshow(tokyostation_image)
#plt.show()

#number_scenes = len(tokyostation_scenes)

# Print all images in specified Zoom range
#for zoom in range (17,18):
#    print(zoom)
#    print_image(tokyostation_scenes, number_scenes, zoom)

for scene in kokkai_scenes:
    print(scene["acquisitionDate"])
    

#zoom=18
#xtile=232839 #東京駅周辺x-18
#ytile=103225 #東京駅周辺y-18

#zoom=18
#imgIndex=8
#xtile=232836 #国会議事堂 周辺？
#ytile=103230 #国会議事堂 周辺？

zoom=18
xtile=232830 #国会議事堂x-18
ytile=103230 #国会議事堂y-18

#zoom=17 
#xtile=116415 #国会議事堂x-17
#ytile=51615 #国会議事堂y-17

asnaro_image = get_ASNARO_image(kokkai_scenes[imgIndex]["entityId"], zoom, xtile, ytile)
io.imshow(asnaro_image)

# Get ASNARO image in series format
def get_ASNARO_series_image(scene_id, zoom, topleft_x, topleft_y, size_x=1, size_y=1):
    img = []
    for y in range(size_y):
        row = []
        for x in range(size_x):
            row.append(get_ASNARO_image(scene_id, zoom, topleft_x + x, topleft_y + y))
        img.append(np.hstack(row))
    return  np.vstack(img)

zoom = 18
imgIndex=8
topleft_x=232830 #国会議事堂x-18
topleft_y=103230 #国会議事堂y-18
#topleft_x = 232829 #国会議事堂 周辺？
#topleft_y = 103231 #国会議事堂 周辺？
size_x = 3
size_y = 3
asnaro_series_image = get_ASNARO_series_image(kokkai_scenes[imgIndex]["entityId"], zoom, topleft_x, topleft_y, size_x, size_y)
io.imshow(asnaro_series_image)

# Get ASNARO image in grid display
def make_grid_image(images, col):
    img = []
    for i in range(math.ceil(len(images)/col)):
        row = []
        for j in range(col):
            index = i*col + j
            if index < len(images):
                row.append(images[index])
            else:
                row.append(np.ones_like(imgs[0])*255)
        img.append(np.hstack(row))
    return np.vstack(img)

imgs = [get_ASNARO_series_image(scene["entityId"], zoom, topleft_x, topleft_y, size_x, size_y) for scene in kokkai_scenes]
plt.rcParams["figure.figsize"] = (12, 12)
io.imshow(make_grid_image(imgs, 4))

from datetime import datetime
from datetime import timezone
from skimage import io
from io import BytesIO
import os, json, requests, math
import numpy as np
import dateutil.parser
import matplotlib.pyplot as plt

TOKEN = "your token here"

# Get TSUBAME scene
def get_tsubame_scene(min_lat, min_lon, max_lat, max_lon):
    url = "https://gisapi.tellusxdp.com/api/v1/tsubame/scene" \
    + "?min_lat={}&min_lon={}&max_lat={}&max_lon={}".format(min_lat, min_lon, max_lat, max_lon)
    headers = {
        "Authorization": "Bearer " + TOKEN
    }
    r = requests.get(url, headers=headers)
    # Check request URL 
    if check_URL(r):
        return r.json()

# Get TSUBAME image
def get_tsubame_image(scene_id, zoom, xtile, ytile):
    url = " https://gisapi.tellusxdp.com/tsubame/{}/{}/{}/{}.png".format(scene_id, zoom, xtile, ytile)
    headers = {
        "Authorization": "Bearer " + TOKEN
    }
    r = requests.get(url, headers=headers)
    # Check request URL 
    if check_URL(r):
        image = io.imread(BytesIO(r.content))
        return image
    #image = io.imread(BytesIO(r.content))
    #return image

# Get TSUBAME image in series format
def get_tsubame_series_image(scene_id, zoom, topleft_x, topleft_y, size_x=1, size_y=1):
    img = []
    for y in range(size_y):
        row = []
        for x in range(size_x):
            row.append(get_tsubame_image(scene_id, zoom, topleft_x + x, topleft_y + y))
        img.append(np.hstack(row))
    return  np.vstack(img)

# Get TSUBAME image in grid display
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

# Function to check the URL and Http request status
def check_URL(reqURL):
    if ((reqURL.status_code == 200)):
        print("URL:", reqURL.url)
        print("Status: ", reqURL.status_code, "OK")
        return True
    elif (reqURL.status_code == 404):
        #print("Status: ", reqURL.status_code, "Not Found")
        return False
    else:
        #print("Status: ", reqURL.status_code, "ERROR: Check your parameter!!")
        return False
    
# Filter dates
def filter_by_date(scenes, start_date=None, end_date=None):
    if(start_date == None):
        start_date = datetime(1900,1,1, tzinfo=timezone.utc)
    if(end_date == None):
        end_date = datetime.now(timezone.utc)
    return [scene for scene in scenes if start_date <= dateutil.parser.parse(scene["acquisitionDate"]) and dateutil.parser.parse(scene["acquisitionDate"]) < end_date]

# Classify areas
def classify(areas, scenes):
    result = [[] for i in range(len(areas))]
    for scene in scenes:
        dists = [np.linalg.norm(np.array([scene["clat"], scene["clon"]]) - np.array([area["lat"], area["lon"]])) for area in areas]
        result[np.argmin(dists)].append(scene)
    for i in range(len(result)):
        result[i] = sorted(result[i], key=lambda scene: dateutil.parser.parse(scene["acquisitionDate"]))
    return result

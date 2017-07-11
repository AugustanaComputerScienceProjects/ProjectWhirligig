# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:19:27 2017

@author: tylermay14
"""

import numpy as np
import cv2
import json
from collections import OrderedDict


def getJSONFromMarkedImageFile(filename):
    if 'medium' in filename:
        beetleBoxSize = 16
    elif 'large' in filename:
        beetleBoxSize = 64
        
    img = cv2.imread(filename)
    height, width, channels = img.shape
    rects = []
    for x in range(width):
        for y in range(height):
            B,G,R = img[y,x]
            if (R == 237) and (G == 28) and (B == 36):
                x1 = x-beetleBoxSize/2
                x2 = x+beetleBoxSize/2
                y1 = y-beetleBoxSize/2
                y2 = y+beetleBoxSize/2
                
                bbox = OrderedDict([("x1",x1),("x2",x2),("y1",y1),("y2",y2)])
                rects.append(bbox)
                
    json_image = OrderedDict([("image_path", filename), ("rects", rects)])
    return json_image




LARGE_TRAINING_SET = ["large1a_frame0151.png" ,"large1a_frame0157.png","large1a_frame0160.png", "large1a_frame0169.png", "large1a_frame0172.png","large1a_frame0175.png", "large2_frame0001_markedHH.png", "large1_frame0001_markedHH.png"]
LARGE_TESTING_SET = ["large1a_frame0154.png", "large1a_frame0166.png","large1a_frame0178.png"] 
MEDIUM_TRAINING_SET = ["medium5_frame0175.png","medium1_frame0001_markedHH.png","medium3_frame0001_markedHH.png","medium4_frame0001_markedHH.png","medium5_frame0001_markedHH.png","medium5_frame0154.png","medium5_frame0157.png","medium5_frame0160.png","medium5_frame0166.png","medium5_frame0169.png","medium5_frame0172.png"]
MEDIUM_TESTING_SET = ["medium2_frame0001_markedHH.png","medium5_frame0163.png","medium5_frame0151.png"]

COMBINED_TRAINING_SET = ["large1a_frame0151.png" ,"large1a_frame0157.png","large1a_frame0160.png", "large1a_frame0169.png", "large1a_frame0172.png","large1a_frame0175.png", "large2_frame0001_markedHH.png", "large1_frame0001_markedHH.png", "medium5_frame0175.png","medium1_frame0001_markedHH.png","medium3_frame0001_markedHH.png","medium4_frame0001_markedHH.png","medium5_frame0001_markedHH.png","medium5_frame0154.png","medium5_frame0157.png","medium5_frame0160.png","medium5_frame0166.png","medium5_frame0169.png","medium5_frame0172.png"]
COMBINED_TESTING_SET = ["large1a_frame0154.png", "large1a_frame0166.png","large1a_frame0178.png","medium2_frame0001_markedHH.png","medium5_frame0163.png","medium5_frame0151.png"]

imageFileNames = LARGE_TRAINING_SET
outfile_name = "beetle_training_large.json"

json_images = []

with open(outfile_name, 'w') as outfile:
    for imageFileName in imageFileNames:
        json_image = getJSONFromMarkedImageFile("marked_frames/" + imageFileName)
        json_images.append(json_image)
    
    
    outfile.write(json.dumps(json_images, indent = 1))

#    outfile.write(json.dumps(json_image, indent = 1))

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:19:27 2017
@author: tylermay14

Takes a marked .png file with red dots on the center of each beetle and creates a .txt file with the coordinates of each red dot
Counts the number of red dots and prints them
"""

import numpy as np
import cv2

imageFileName = 'marked_frames/large1_frame0001_markedHH.png'
textFileName = imageFileName.replace('.png', '') + '.txt'

img = cv2.imread(imageFileName)

lower_thresh_red = np.array([0,0,174])
upper_thresh_red = np.array([50,75,255])
mask_red = cv2.inRange(img, lower_thresh_red, upper_thresh_red)
    
cnts = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

with open(textFileName, 'w') as fout:
    counter = 0
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        fout.write(str(x) + ' ' + str(y) + '\n')
        counter +=1

print("# of red pixels: ", counter)


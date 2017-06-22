# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:19:27 2017

@author: tylermay14
"""

import numpy as np
import cv2

imageFileName = 'medium3_frame0001_markedHH.png'
textFileName = imageFileName.replace('.png', '') + '.txt'

img = cv2.imread(imageFileName)

height, width, channels = img.shape

with open(textFileName, 'w') as fout:
    counter = 0
    for x in range(width):
        for y in range(height):
            if (img.item(y,x,2) ==237) and (img.item(y,x,1) ==28) and (img.item(y,x,0) ==36):
                fout.write(str(x) + ' ' + str(y) + '\n')
                counter +=1


print("# of red pixels: ", counter)


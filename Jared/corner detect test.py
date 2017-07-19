# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:39:05 2017

@author: jaredhaeme15
"""


import cv2
import numpy as np
from collections import deque
import imutils
import misc_image_tools 

frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4"
cap = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4")
    
while(1): 
       
    successFlag, frame = cap.read()
    if not successFlag:
        cv2.waitKey(0)
        break 
    lower_hsv_thresholdcr = np.array([0,250,250])
    upper_hsv_thresholdcr = np.array([10,255,255])
    gray = np.float32(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
    dst = cv2.cornerHarris(gray,2,3,0.04)
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    frameWithRedCorners = np.copy(frame)
    # Threshold for an optimal value, it may vary depending on the image.
    frameWithRedCorners[dst>0.005*dst.max()]=[0,0,255]
    hsv = cv2.cvtColor(frameWithRedCorners, cv2.COLOR_BGR2HSV)
    #construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    crmask = cv2.inRange(hsv, lower_hsv_thresholdcr, upper_hsv_thresholdcr)
    cntscr = cv2.findContours(crmask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
    cv2.imshow("Frame", frameWithRedCorners)
    k = cv2.waitKey(10000) & 0xFF
    if k == 27:  # esc key
        break
cv2.destroyAllWindows()
cap.release()
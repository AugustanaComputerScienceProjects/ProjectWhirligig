
# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import cv2
import numpy as np
from collections import deque
import imutils

import misc_image_tools 


frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5.mp4"
textFileName = frameFileName.replace('.mp4', '') + 'MultipleMethods.txt'


# then initialize the
# list of tracked points


def find_beetles_in_group(cnt):
    #gray = cv2.cvtColor(cnt,cv2.COLOR_BGR2GRAY)
   
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(cnt,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.01*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    markers = cv2.watershed(cnt,markers)
    m = cv2.convertScaleAbs(markers)
    ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    return cnts
def find_beetles_by_color(frame):
    locthresh=[]
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cntsthresh = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    # process each contour in our contour list
    for c in cntsthresh:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 5 and radius <40:
            if radius > 15:
                for ct in find_beetles_in_group(c):
                    ((x, y), radius) = cv2.minEnclosingCircle(ct)
                    locthresh.append((x,y))
            locthresh.append((x,y))
    return locthresh

def find_beetles_by_corners(frame):
    loccr=[]
    lower_hsv_thresholdcr = np.array([0,250,250])
    upper_hsv_thresholdcr = np.array([10,255,255])
    gray = np.float32(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
    dst = cv2.cornerHarris(gray,2,3,0.04)
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    frameWithRedCorners = np.copy(frame)
    # Threshold for an optimal value, it may vary depending on the image.
    frameWithRedCorners[dst>0.01*dst.max()]=[0,0,255]
    hsv = cv2.cvtColor(frameWithRedCorners, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    crmask = cv2.inRange(hsv, lower_hsv_thresholdcr, upper_hsv_thresholdcr)
    cntscr = cv2.findContours(crmask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
     # process each contour in our contour list
    for c in cntscr:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
       
        if radius > 0 and radius <30:
            #if radius > 15: 
            loccr.append((x,y))
    return loccr

def matches(xm, ym, xt, yt):
    return ((xt-7) <= xm <= (xt+7)) and yt-7 <= ym <= yt+7



cap = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5.mp4")

while(1): 
    matched=[]
    successFlag, frame = cap.read()
    if not successFlag:
        cv2.waitKey(0)
        break 
    locthresh=find_beetles_by_color(frame)
    loccr=find_beetles_by_corners(frame)
   
    for xm, ym in locthresh:
        for xt, yt in loccr:
            if matches(xm, ym, xt, yt):
                matched.append((xm,ym))

    print ("Matched length:"+str(len(set(matched))))
    print ("Corner detect length:"+ str(len(loccr)))
    print ("Thresh detect length:" +str(len(locthresh)))
    with open(textFileName, 'w') as fout:
        for x,y in set(matched):
        # draw a circle at each x,y that matched using cv2.circle
            cv2.circle(frame, (int (x),int (y)), 5, (0, 255, 255), -1)
            fout.write(str(x) + ' ' + str(y) + '\n')

    frame = imutils.resize(frame, width=720, height=540)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # esc key
        break
cv2.destroyAllWindows()
cap.release()


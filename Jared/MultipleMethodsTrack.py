
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


# returns a LIST of small contours resulting from eroding one large contour
def splitMultipleBeetles(maskImage, bigContour):
    x,y,w,h = cv2.boundingRect(bigContour)
    cropped = maskImage[y:(y + h),x:(x + w)]
    #kernel = np.ones((3,3),np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    eroded=cv2.erode(cropped, kernel, iterations=1)
    cnts = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    for cnt in cnts:
        cnt += np.array([x,y])
    return cnts
    
def find_beetles_by_color(frame):
    locthresh=[]
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, np.array([0,0,0]), np.array([200,200,47]))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    #thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    cv2.imshow("thresh", thresh)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cntsthresh = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    improvedContourList = []
    for c in cntsthresh:
        ((x, y), radius) = cv2.minEnclosingCircle(c)           
        if 15 < radius <= 40:
            improvedContourList.extend(splitMultipleBeetles(thresh,c))
        else:
            improvedContourList.append(c)
          

    # process each contour in our contour list
    for c in improvedContourList:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if 5 < radius <= 20:
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
    frameWithRedCorners[dst>0.015*dst.max()]=[0,0,255]
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

    frame = imutils.resize(frame, width=1000, height=800)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # esc key
        break
cv2.destroyAllWindows()
cap.release()


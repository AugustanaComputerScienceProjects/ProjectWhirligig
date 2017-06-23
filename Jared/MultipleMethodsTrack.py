
# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import cv2
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

def matches(xm, ym, xt, yt):
    return ((xt-5) <= xm <= (xt+5)) and yt-5 <= ym <= yt+5
frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5.mp4"
textFileName = frameFileName.replace('.mp4', '') + '.txt'

lower_hsv_threshold = np.array([0,0,0])
upper_hsv_threshold = np.array([200,200,47])

lower_hsv_thresholdcr = np.array([0,250,250])
upper_hsv_thresholdcr = np.array([10,255,255])
# then initialize the
# list of tracked points
BUFFER_SIZE = 125
pts = deque(maxlen=BUFFER_SIZE)

def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

loccr=[]
locthresh=[]
matched=[]
cap = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5.mp4")


fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("harriscorner2.avi", fourcc, 20.0, (1440, 1080))
print (out.isOpened())  # True = write out video successfully. False - fail to write out video.

while(1):

    successFlag, frame = cap.read()
    if not successFlag:
        cv2.waitKey(0)
        break
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    frame[dst>0.01*dst.max()]=[0,0,255]
    
    #cv2.imshow('dst',frame)
    
    
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    crmask = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    crmask2 = cv2.dilate(crmask, None, iterations=2)
    crmask3 = cv2.erode(crmask2, None, iterations=1)
    cv2.imshow("mask", crmask2)

    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    mask2 = cv2.erode(mask, None, iterations=2)
    mask3 = cv2.dilate(mask2, None, iterations=2)
   
    gray1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray1,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #cv2.imshow('thresh',thresh)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    sure_bg = cv2.dilate(opening,kernel,iterations=5)
    #cv2.imshow('sure_bg' ,sure_bg)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.01*dist_transform.max(),255,0)
    #cv2.imshow('sure_fg' ,sure_fg)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    #cv2.imshow('sure_fg' ,sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    #cv2.imshow('unknown', unknown)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    #cv2.imshow('markers', markers)
 
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cntsthresh = cv2.findContours(sure_fg.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    cntscr = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    
    #frame=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # process each contour in our contour list
    for c in cntscr:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
            # only proceed if the radius meets a minimum size
        if radius > 5 and radius <30:
            x=center[0]
            y=center[1]
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.circle(frame, (int(x), int(y)), int(radius),
                    #(0, 255, 255), 2)
            #cv2.circle(frame, center, 5, (0, 255, 255), -1)
 
                # update the points queue
            loccr.append(center)
            
            
            # process each contour in our contour list
    for c in cntsthresh:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
            # only proceed if the radius meets a minimum size
        if radius > 5 and radius <30:
            x=center[0]
            y=center[1]
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.circle(frame, (int(x), int(y)), int(radius),
                    #(0, 255, 255), 2)
            #cv2.circle(frame, center, 5, (0, 255, 255), -1)
 
                # update the points queue
            locthresh.append(center)
    for xm, ym in loccr:
        for xt, yt in locthresh:
            if matches(xm, ym, xt, yt):
                matched.append((xm,ym))
    plt.scatter(*zip(*matched), c='g', s=3)
    
    out.write(frame)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(10000000) & 0xFF
    if k == 27:  # esc key
        break

cv2.destroyAllWindows()
cap.release()
out.release()


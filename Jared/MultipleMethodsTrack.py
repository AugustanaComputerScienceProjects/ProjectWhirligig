
# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import cv2
import numpy as np
from collections import deque
import imutils

def matches(xm, ym, xt, yt):
    return ((xt-7) <= xm <= (xt+7)) and yt-7 <= ym <= yt+7

frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5.mp4"
textFileName = frameFileName.replace('.mp4', '') + 'MultipleMethods.txt'

lower_hsv_threshold = np.array([0,0,0])
upper_hsv_threshold = np.array([200,200,60])

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


cap = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium2.mp4")


while(1):
    loccr=[]
    locthresh=[]
    locedge=[]
    matched=[]
    successFlag, frame = cap.read()
    if not successFlag:
        cv2.waitKey(0)
        break
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    
    frameWithRedCorners = np.copy(frame)
    
    # Threshold for an optimal value, it may vary depending on the image.
    frameWithRedCorners[dst>0.01*dst.max()]=[0,0,255]
    
    #cv2.imshow('dst',frame)
    #cv2.imshow("framecr", frameWithRedCorners)
    
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frameWithRedCorners, cv2.COLOR_BGR2HSV)
    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    crmask = cv2.inRange(hsv, lower_hsv_thresholdcr, upper_hsv_thresholdcr)
    #crmask2 = cv2.dilate(crmask, None, iterations=2)
    #crmask3 = cv2.erode(crmask2, None, iterations=1)
    #cv2.imshow("crmask", crmask)

    
    
    gray1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray1,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
   
    

 
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cntsthresh = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    
    cntscr = cv2.findContours(crmask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    #frame=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # process each contour in our contour list
    for c in cntscr:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
       
        if radius > 0 and radius <30:
               
            loccr.append((x,y))
            
            
            # process each contour in our contour list
    for c in cntsthresh:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 5 and radius <40:
            locthresh.append((x,y))
            #cv2.circle(frame, (int (x),int (y)), 5, (0, 255, 255), -1) 
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
    
    #frame = imutils.resize(frame, width=720, height=540)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # esc key
        break
cv2.destroyAllWindows()
cap.release()



# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import cv2
import numpy as np
from collections import deque


def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


cap = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium1.mp4")


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
    
    lower_hsv_threshold = np.array([0,250,250])
    upper_hsv_threshold = np.array([10,255,255])

    # then initialize the
    # list of tracked points
    BUFFER_SIZE = 125
    pts = deque(maxlen=BUFFER_SIZE)
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    mask2 = cv2.dilate(mask, None, iterations=2)
    mask3 = cv2.erode(mask2, None, iterations=1)
    cv2.imshow("mask", mask2)

 
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    #frame=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # process each contour in our contour list
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #M = cv2.moments(c)
        #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 5 and radius <30:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
            #cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
            # update the points queue
            pts.appendleft(center)

    # loop over the set of tracked points
    for i in np.arange(0, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        #if pts[i - 1] is None or pts[i] is None:
        #    continue
 
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        #thickness = int(np.sqrt(BUFFER_SIZE / float(i + 1)) * 2.5)
        thickness = int(np.sqrt(BUFFER_SIZE - i) / 3 + 2)
        #cv2.circle(frame, pts[i], thickness, (0, 0, 255), -1)

        #cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    
    out.write(frame)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # esc key
        break

cv2.destroyAllWindows()
cap.release()
out.release()
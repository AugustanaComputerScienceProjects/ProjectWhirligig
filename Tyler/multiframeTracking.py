# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:27:29 2017

@author: tylermay14
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:12:48 2017
@author: kylemccaw15
"""

# Python 2/3 compatibility
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    long = int

from math import cos, sin, sqrt
import numpy as np
import cv2
import sys
 
if __name__ == '__main__' :
 
    # Implementing Kalman Filter
    img_height = 1080
    img_width = 1920
    kalman = cv2.KalmanFilter(2, 1, 0)
    
    # Set up tracker.
    # Instead of MIL, you can also use
    # BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
     
    tracker = cv2.Tracker_create("MEDIANFLOW")
 
    # Read video
    video = cv2.VideoCapture("S:/CLASS/CS/ProjectWhirligig/videos/large1.MP4")
 
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    bbox = (315, 9, 40, 55)
 
    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Draw bounding box
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,0,255))
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(100) & 0xff
        if k == 27 : break
    cv2.destroyAllWindows()
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np
from collections import deque
import imutils
import MediumVideoSingleFrameDetection as md
import LargeVideoSingleFrameDetection as ld
from MarkedvsTrackedAccuracyDetector import distanceSquared

def getFindingMethod(filename):
    if 'large' in filename:
        return ld.find_beetles_by_color
    elif 'medium' in filename:
        return md.find_beetles_combined
    else:
        raise Exception("I don't know what method to use for " + filename)
    
if __name__ == '__main__':
    filename="large1.mp4"
    cap = cv2.VideoCapture("H:\\ProjectWhirligig\\" + filename)
    
    successFlag, frame = cap.read()
    #successFlag, frame1 = cap.read()
    findingFunction = getFindingMethod(filename)
    prevLocations = findingFunction(frame)
    
    while(True): 
        successFlag, frame = cap.read()
        if not successFlag:
            cv2.waitKey(0)
            break 
        
        curLocations = findingFunction(frame)
        
        
        print ("Matched length:"+str(len(set(matched))))
        
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
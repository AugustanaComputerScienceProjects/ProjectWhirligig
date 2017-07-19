"""This program was made to analyze video medium5.mp4 by looking at each frame 
and detecting all the beetles in that frame and their coordinates. However it 
does not find the identies of beetles. This program uses corner detection and
thresholding algorithim together and looks for matches between the lists. 
It also takes beetles that are too close together and splits them up so they 
are not tracked as one beetle"""

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
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    eroded=cv2.erode(cropped, kernel, iterations=1)
    cnts = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    for cnt in cnts:
        cnt += np.array([x,y])
    return cnts
 
#Returns a list of the coordinates of the beetles detected by
#the thresholding algorithim    
def find_beetles_by_threshold(frame):
    locthresh=[]
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
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

#Returns a list of coordinats of the beetles detected by the corner
#detection
def find_beetles_by_corners(frame):
    loccr=[]
    lower_hsv_thresholdcr = np.array([0,250,250])
    upper_hsv_thresholdcr = np.array([10,255,255])
    gray = np.float32(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
    dst = cv2.cornerHarris(gray,2,3,0.04)
    frameWithRedCorners = np.copy(frame)
    frameWithRedCorners[dst>0.015*dst.max()]=[0,0,255]
    hsv = cv2.cvtColor(frameWithRedCorners, cv2.COLOR_BGR2HSV)
    crmask = cv2.inRange(hsv, lower_hsv_thresholdcr, upper_hsv_thresholdcr)
    cntscr = cv2.findContours(crmask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
     # process each contour in our contour list
    for c in cntscr:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 0 and radius <30:
            loccr.append((x,y))
    return loccr

#goes through list of the thresholding coordinates and 
#corner detected coordinates and looks for matches 
def find_beetles_combined(frame):
    matched=[]
    locthresh=find_beetles_by_threshold(frame)
    loccr=find_beetles_by_corners(frame)
    for xm, ym in locthresh:
        for xt, yt in loccr:
            if matches(xm, ym, xt, yt):
                matched.append((xm,ym))
#    print ("Corner detect length:"+ str(len(loccr)))
#    print ("Thresh detect length:" +str(len(locthresh)))
    return matched

def matches(xm, ym, xt, yt):
    return ((xt-7) <= xm <= (xt+7)) and yt-7 <= ym <= yt+7

if __name__ == '__main__':
    cap = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5.mp4")
    
    while(1): 
       
        successFlag, frame = cap.read()
        if not successFlag:
            cv2.waitKey(0)
            break 
        matched=find_beetles_combined(frame)
        
        print ("Matched length:"+str(len(set(matched))))
        
        with open(textFileName, 'w') as fout:
            for x,y in set(matched):
            # draw a circle at each x,y that matched using cv2.circle
                cv2.circle(frame, (int (x),int (y)), 5, (0, 255, 255), -1)
                fout.write(str(x) + ' ' + str(y) + '\n')
    
        #frame = imutils.resize(frame, width=1000, height=800)
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(10000) & 0xFF
        if k == 27:  # esc key
            break
    cv2.destroyAllWindows()
    cap.release()
    

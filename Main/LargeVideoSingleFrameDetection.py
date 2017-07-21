# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 13:56:23 2017

@author: jaredhaeme15
"""
import numpy as np
import cv2
import imutils

def matches(xm, ym, xt, yt):
    return ((xt-7) <= xm <= (xt+7)) and yt-7 <= ym <= yt+7


def find_beetles_by_color(frame):
    lower_hsv_thresholdcr = np.array([0,250,250])
    upper_hsv_thresholdcr = np.array([10,255,255])
    gray = np.float32(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
    dst = cv2.cornerHarris(gray,5,5,0.00000004)
    frameWithRedCorners = np.copy(frame)
    frameWithRedCorners[dst>0.0004*dst.max()]=[0,0,255]
    hsv = cv2.cvtColor(frameWithRedCorners, cv2.COLOR_BGR2HSV)
    crmask = cv2.inRange(hsv, lower_hsv_thresholdcr, upper_hsv_thresholdcr)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    crmask2 = cv2.morphologyEx(crmask, cv2.MORPH_CLOSE, kernel, iterations=20)
    crmask3 = cv2.morphologyEx(crmask2,cv2.MORPH_OPEN,kernel, iterations = 10)
    cv2.imshow("crmask", crmask)
    cv2.imshow("cr", frameWithRedCorners)
    #looks for middle part of beetles
    mask_mid = cv2.inRange(frame, np.array([10,10,120]),np.array([250,250,250]))
    #cv2.imshow("mask_mid", mask_mid)
    
    #Creates threshold mask that gives beetle shapes but picks up waves
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #Finds red blue and dark green pixel color on beetle
    mask_dark_green = cv2.inRange(frame, np.array([0,0,0]), np.array([255,37,255]))
    
    #Finds lighter reflections on beetles
    mask_light=cv2.inRange(frame, np.array([100,105,100]), np.array([200,200,200]))
   
    #finds middle colors of beeltes which gives outline of beetle
    mask_outline=cv2.inRange(frame, np.array([50,50,35]), np.array([100,105,150]))
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    mask_dark_green2 = cv2.morphologyEx(mask_dark_green,cv2.MORPH_OPEN,kernel, iterations = 1)
    #cv2.imshow("erode", mask2)
    mask_dark_green3 = cv2.dilate(mask_dark_green2, kernel, iterations=5)
    
    #Combines all the masks together
    combinedMask = cv2.bitwise_or(mask_dark_green3,thresh)
    combinedMask= cv2.bitwise_or(combinedMask, mask_light)
    combinedMask=cv2.bitwise_or(combinedMask, mask_mid)
    #combinedMask=cv2.bitwise_or(combinedMask, crmask)
    combinedMask=cv2.bitwise_or(combinedMask,mask_outline, mask=crmask3)
    cv2.imshow("combinedMask", combinedMask)
    closing = cv2.morphologyEx(combinedMask, cv2.MORPH_CLOSE, kernel, iterations=3)
    opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel, iterations = 2)

    cv2.imshow("closing", opening)
    # find contours in the mask 
    cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    coords = []
    improvedContourList = []
    count=0
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)          
        if 35 < radius <= 100:
            count+=1
            improvedContourList.extend(splitMultipleBeetles(frame,c))
            print (count)
        else:
            improvedContourList.append(c)
          
            
    # process each contour in our contour list
    for c in improvedContourList:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if 10 < radius <= 35:
            coords.append((x,y))
            
    #mask_dark_green=imutils.resize(mask_dark_green, width=1080, height=810)
    #cv2.imshow("Mask Dark", mask_dark_green)
    
    #mask_light=imutils.resize(mask_light, width=1080, height=810)
    #cv2.imshow("Mask Light", mask_light)
    
    #mask_outline=imutils.resize(mask_outline, width=1080, height=810)
    #cv2.imshow("Mask outline", mask_outline)
    return coords

#Takes in large contours (beetles close together) and lookes for middle parts 
#of beetles to split beetles apart
def splitMultipleBeetles(frame, bigContour):
   x,y,w,h = cv2.boundingRect(bigContour)
   cropped = frame[y:(y + h),x:(x + w)]
   mask_dark_green = cv2.inRange(cropped, np.array([0,0,0]), np.array([255,37,255]))
   mask_mid = cv2.inRange(cropped, np.array([10,10,120]), np.array([250,250,250]))
   combinedSmall=cv2.bitwise_or(mask_dark_green, mask_mid)
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   combinedSmall = cv2.morphologyEx(combinedSmall, cv2.MORPH_CLOSE, kernel, iterations=3)
   combinedSmall = cv2.morphologyEx(combinedSmall,cv2.MORPH_OPEN,kernel, iterations = 2)
   cnts = cv2.findContours(combinedSmall.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
   for cnt in cnts:
       #((x, y), radius) = cv2.minEnclosingCircle(cnt)
       #cv2.circle(frame, (int(x), int(y)), int(radius),
        #            (0, 255, 255), 2)
       cnt += np.array([x,y])
   return cnts   
CHECK_FRAME_LIST = [1] + list(range(151,178+1,3))
if __name__ == '__main__':
    frameFileName = r"H:\ProjectWhirligig\large1.mp4"
    # then initialize the
    # list of tracked points
    textFileName = frameFileName.replace('.mp4', '');

    
    
    camera = cv2.VideoCapture(r"H:\ProjectWhirligig\large1.mp4")
   
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter("LargeVideoSingleFrameDetection.avi", fourcc, 20.0, (1080, 810))
    

    camera = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4")

    frameNum = 0
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        frameNum += 1
        if not grabbed:
            break
        coords = find_beetles_by_color(frame)
        if frameNum in CHECK_FRAME_LIST:
            # process each contour in our contour list
            with open("%s_frame%04d_predicted.txt"%(textFileName,frameNum) , 'w') as fout:
                for x,y in coords:
                    fout.write(str(x) + ' ' + str(y) + '\n')
        for x,y in coords:
            cv2.circle(frame, (int (x), int (y)), 5, (0, 0, 255), -1)
        # show the frame to our screen
        frame = imutils.resize(frame, width=1080, height=810)
        cv2.imshow("Frame", frame)

        out.write(frame)
       
    
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break 
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
    out.release()
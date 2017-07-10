# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np


def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


cap = cv2.VideoCapture("H:/ProjectWhirligig/medium1.mp4")

prevFrame = create_blank(1440, 1080, (255, 255, 255))

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("harriscorner3.avi", fourcc, 20.0, (1440, 1080))
print (out.isOpened())  # True = write out video successfully. False - fail to write out video.

while(1):

    successFlag, frame = cap.read()
    if not successFlag:
        cv2.waitKey(0)
        break
#    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#    
#    lower_red = np.array([0,0,0])
#    upper_red = np.array([255,255,60])
#    
#    mask = cv2.inRange(hsv, lower_red, upper_red)
#    cv2.imshow('mask',mask)
#    
#    whiteImage = create_blank(1440, 1080, (255, 255, 255))
#    res = cv2.bitwise_and(frame,frame,whiteImage,mask= mask)
#    cv2.imshow('res',res)
#
#    diff = cv2.absdiff(frame,prevFrame)
#    cv2.imshow('diff',diff)

#
#
#    cv2.imshow('Original',frame)
#    edges = cv2.Canny(frame,100,200)
#    
#    gray = cv2.cvtColor(edges,cv2.COLOR_BGR2GRAY)
#    gray = np.float32(gray)
#    dst = cv2.cornerHarris(gray,2,3,0.04)
#    
#    #result is dilated for marking the corners, not important
#    dst = cv2.dilate(dst,None)
#
#    # Threshold for an optimal value, it may vary depending on the image.
#    frame[dst>0.01*dst.max()]=[0,0,255]
#    
#    cv2.imshow('dst',frame)
#    prevFrame = frame
#    #edgeSmall = cv2.resize(edges,(360,270), interpolation = cv2.INTER_CUBIC)
#    #edgeSmall = cv2.cvtColor(edgeSmall, cv2.COLOR_GRAY2BGR)
#    #out.write(edgeSmall)
#    out.write(frame)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)
    
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    
    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
    
    # Now draw them
    res = np.hstack((centroids,corners))
    res = np.int0(res)
    frame[res[:,1],res[:,0]]=[0,0,255]
    frame[res[:,3],res[:,2]] = [0,255,0]
    
    cv2.imshow('dst',frame)
    prevFrame = frame
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # esc key
        break

cv2.destroyAllWindows()
cap.release()
out.release()
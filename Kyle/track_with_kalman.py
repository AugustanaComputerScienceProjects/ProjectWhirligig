# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:29:59 2017

@author: kylemccaw15
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

file="H:\Summer Research\ProjectWhirligig\Kyle\videos\large2.mp4"
capture = cv2.VideoCapture(file)
#print("\t Width: ",capture.get(cv2.VideoCapture.__getattribute__(CV_CAP_PROP_FRAME_WIDTH)))
#print("\t Height: ",capture.get(cv2.VideoCapture.__getattribute__(CV_CAP_PROP_FRAME_HEIGHT)))
#print("\t FourCC: ",capture.get(cv2.VideoCapture.__getattribute__(CV_CAP_PROP_FOURCC)))
#print("\t Framerate: ",capture.get(cv2.VideoCapture.__getattribute__(CV_CAP_PROP_FPS)))
numframes=capture.get(7)
print("\t Number of Frames: ",numframes)

count = 0
history = 10
nGauss = 3
bgThresh = 0.6
noise = 20
#bgs = cv2.createBackgroundSubtractorMOG2(history,nGauss,bgThresh,noise)
bgs = cv2.createBackgroundSubtractorMOG2()

plt.figure()
plt.hold(True)
plt.axis([0,480,360,0])

measuredTrack=np.zeros((numframes,2)-1
                       
while (count<numframes):
    count+=1
    img2 = capture.read()[1]
    cv2.imshow("Video",img2)
    foremat=bgs.apply(img2)
    cv2.waitKey(100)
    foremat=bgs.apply(img2)
    ret,thresh = cv2.threshold(foremat,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        m= np.mean(contours[0],axis=0)
        measuredTrack[count-1,:]=m[0]
        plt.plot(m[0,0],m[0,1],'ob')
    cv2.imshow('Foreground',foremat)
    cv2.waitKey(80)
capture.release()
print(measuredTrack)
np.save("beetlesTwoTest", measuredTrack)
plt.show()
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

inputVideo = cv2.VideoCapture(r'S:\CLASS\CS\ProjectWhirligig\videos\large1.mp4')
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
prevFrame = create_blank(1440, 1080, (255, 255, 255))


history = 1000

while (1):
    retVal, frame = inputVideo.read()
    if not retVal:
        break

    fgmask = fgbg.apply(frame, learningRate=10.0/history)

    cv2.imshow('Foreground', fgmask)
    cv2.imshow('Original', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()
inputVideo.release()

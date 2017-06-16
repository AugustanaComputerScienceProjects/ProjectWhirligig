import cv2
import numpy as np
from matplotlib import pyplot as plt


def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


cap = cv2.VideoCapture("H:/Project Whiriligig/opencvtesting/medium1.mp4")

prevFrame = create_blank(1440, 1080, (255, 255, 255))

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("C:/Users/jaredhaeme15/Desktop/edges.avi", fourcc, 20.0, (1440, 1080))
print (out.isOpened())  # True = write out video successfully. False - fail to write out video.

while(1):

    successFlag, frame = cap.read()
    if not successFlag:
        cv2.waitKey(0)
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([0,0,0])
    upper_red = np.array([255,255,60])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    res = cv2.bitwise_and(frame,frame,mask= mask)
    
   

    


    cv2.imshow('Original',frame)
    edges = cv2.Canny(frame,100,200)
    #cv2.imshow('Edges',edges)
    
    edges=cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    
    overlay = cv2.bitwise_or(frame,edges)
    #cv2.imshow('overlay',overlay)
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('thresh',thresh)
    
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    cv2.imshow('opening' ,opening)
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    cv2.imshow('sure_bg' ,sure_bg)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    cv2.imshow('sure_fg' ,sure_fg)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)


    #cv2.imshow('markers', markers)
    
    
    #edgeSmall = cv2.resize(edges,(360,270), interpolation = cv2.INTER_CUBIC)
    #edgeSmall = cv2.cvtColor(edgeSmall, cv2.COLOR_GRAY2BGR)
    #out.write(edgeSmall)
    out.write(overlay)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # esc key
        break

cv2.destroyAllWindows()
cap.release()
out.release()
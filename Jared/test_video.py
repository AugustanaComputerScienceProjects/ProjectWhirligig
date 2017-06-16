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


cap = cv2.VideoCapture("H:/Project Whiriligig/opencvtesting/large1.mp4")

prevFrame = create_blank(1440, 1080, (255, 255, 255))

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("edges.avi", fourcc, 20.0, (1440, 1080))
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
    cv2.imshow('mask',mask)
    
    whiteImage = create_blank(1440, 1080, (255, 255, 255))
    res = cv2.bitwise_and(frame,frame,whiteImage,mask= mask)
    cv2.imshow('res',res)

    diff = cv2.absdiff(frame,prevFrame)
    cv2.imshow('diff',diff)
    prevFrame = frame
    


    cv2.imshow('Original',frame)
    edges = cv2.Canny(frame,100,200)
    cv2.imshow('Edges',edges)
    
    #edgeSmall = cv2.resize(edges,(360,270), interpolation = cv2.INTER_CUBIC)
    #edgeSmall = cv2.cvtColor(edgeSmall, cv2.COLOR_GRAY2BGR)
    #out.write(edgeSmall)
    out.write(cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR))

    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # esc key
        break

cv2.destroyAllWindows()
cap.release()
out.release()
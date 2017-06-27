
# import the necessary packages
from collections import deque
import numpy as np
import cv2
 

# define the lower and upper boundaries of the 
# whirligig beetles (using the HSV color space)
lower_hsv_threshold = np.array([0,0,0])
upper_hsv_threshold = np.array([255,255,50])

# then initialize the
# list of tracked points
BUFFER_SIZE = 0
pts = deque(maxlen=BUFFER_SIZE)
 
#camera = cv2.VideoCapture("C:/Users/jaredhaeme15/Downloads/Moving Ball.mp4")
camera = cv2.VideoCapture(r"H:\Project Whiriligig\opencvtesting\medium2.mp4")


while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    if not grabbed:
        break
 

    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    mask2 = cv2.erode(mask, None, iterations=2)
    mask3 = cv2.dilate(mask2, None, iterations=2)
   
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    sure_bg = cv2.dilate(opening,kernel,iterations=5)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.01*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    cv2.imshow('sure_fg' ,sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
 
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(sure_fg.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    
    
    #frame=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # process each contour in our contour list
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
 
        # only proceed if the radius meets a minimum size
        if radius < 15 and radius > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
 

    cv2.imshow("Frame", frame)
    # show the frame to our screen
    
    key = cv2.waitKey(10) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
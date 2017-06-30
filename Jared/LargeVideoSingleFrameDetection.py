
# import the necessary packages
from collections import deque
import numpy as np
import cv2
import imutils

def find_beetles_by_color(frame):
    # define the lower and upper boundaries of the 
    # whirligig beetles (using the HSV color space)
    lower_hsv_threshold = np.array([0,0,0])
    upper_hsv_threshold = np.array([200,200,47])

    # convert it to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask based on hsv color range, then perform
    # a series of erode and dilations to remove any small
    # blobs left in the mask and merge small blogs into biggers ones
    mask = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    mask2 = cv2.erode(mask, kernel, iterations=1)
    mask3 = cv2.dilate(mask2, kernel, iterations=6)

    # find contours in the mask 
    cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    coords = []
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        # only proceed if the radius meets a minimum size
        if radius > 10 and radius < 40:
            coords.append((x,y))
            #box = cv2.boxPoints(cv2.minAreaRect(c))
            #cv2.drawContours(frame,[np.int0(box)],0,(0,0,255),2)
            #cv2.circle(frame, (int(x), int(y)), int(radius),
                   # (0, 255, 255), 2)


    return coords

    
 

if __name__ == '__main__':
    frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4"
    # then initialize the
    # list of tracked points
    textFileName = frameFileName.replace('.mp4', '') + '.txt'
    
    
    camera = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4")
    
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        
        if not grabbed:
            break
 
        coords = find_beetles_by_color(frame)
        
        # process each contour in our contour list
        with open(textFileName, 'w') as fout:
            for x,y in coords:
                fout.write(str(x) + ' ' + str(y) + '\n')
                cv2.circle(frame, (int (x), int (y)), 5, (0, 0, 255), -1)
                
        # show the frame to our screen
        frame = imutils.resize(frame, width=720, height=540)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        #cv2.imshow("Mask2", mask2)
        cv2.imshow("Mask3", mask3)
        
        key = cv2.waitKey(1) & 0xFF
     
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
     
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
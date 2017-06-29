
# import the necessary packages
from collections import deque
import numpy as np
import cv2
import imutils
 
def distanceSquared(pt1, pt2):
    x1,y1=pt1
    x2,y2=pt2
    return (x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)

# define the lower and upper boundaries of the 
# whirligig beetles (using the HSV color space)
lower_hsv_threshold = np.array([0,0,0])
upper_hsv_threshold = np.array([200,200,47])


frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4"
# then initialize the
# list of tracked points
textFileName = frameFileName.replace('.mp4', '') + '.txt'
camera = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4")
beetle={}
while True:
    currentloc=[]
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    if not grabbed:
        break
 

    # resize the frame, blur it, and convert it to the HSV
    # color space
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    edges = cv2.Canny(frame,100,200)
    cv2.imshow('Edges',edges)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    mask = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    mask2 = cv2.erode(mask, kernel, iterations=1)
    mask3 = cv2.dilate(mask2, kernel, iterations=6)

 
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    #center = None
    
    #frame=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # process each contour in our contour list
    with open(textFileName, 'w') as fout:
        count = 0
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            #M = cv2.moments(c)
            #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        
 
        # only proceed if the radius meets a minimum size
            if radius > 10 and radius < 40:
                
                #rect = cv2.minAreaRect(c)
                #box = cv2.boxPoints(rect)
                #box = np.int0(box)
                #cv2.drawContours(frame,[box],0,(0,0,255),2)
                fout.write(str(x) + ' ' + str(y) + '\n')
            
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(x), int(y)), int(radius),
                   # (0, 255, 255), 2)
                cv2.circle(frame, (int (x), int (y)), 5, (0, 0, 255), -1)
            #print (str(count)+"."+str(center))
            # update the points queue
            #pts.appendleft(center)
                currentloc.append((x,y))
                count += 1
            
    #print (loc)        
    #print ("Beetle number: "+str(len(loc)))
    previousloc=currentloc.copy()
    velocity=set(currentloc)-set(previousloc)
    predicted=set(currentloc)+set(velocity)
    for c in currentloc:
        min(predicted, key=lambda pt: distanceSquared(pt,c))
        
    print (previousloc)
    
    
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
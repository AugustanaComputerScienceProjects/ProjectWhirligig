
# import the necessary packages
from collections import deque
import numpy as np
import cv2
import imutils
 

# define the lower and upper boundaries of the 
# whirligig beetles (using the HSV color space)
lower_hsv_threshold = np.array([0,0,0])
upper_hsv_threshold = np.array([200,200,47])


frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4"
# then initialize the
# list of tracked points
BUFFER_SIZE =75
 
pts = deque(maxlen=BUFFER_SIZE)
loc=[]
textFileName = frameFileName.replace('.mp4', '') + '.txt'

(dX, dY) = (0, 0)


camera = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4")


while True:
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
    mask = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    mask2 = cv2.erode(mask, None, iterations=1)
    mask3 = cv2.dilate(mask2, None, iterations=5)
    # noise removal
    kernel = np.ones((2,2),np.uint8)
    opening = cv2.morphologyEx(mask3,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    
    markers = cv2.watershed(frame,markers)
    frame[markers == -1] = [255,0,0]
    cv2.imshow("Frame", frame)
    cv2.imshow("bg", sure_bg)
    cv2.imshow("fg", sure_fg)

 
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    #frame=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # process each contour in our contour list
    with open(textFileName, 'w') as fout:
        count = 0
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
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
                loc.append(center)
                count += 1
            
    #print (loc)        
    print ("Beetle number: "+str(len(loc)))
    del loc[:]
    
    
    # show the frame to our screen
    frame = imutils.resize(frame, width=720, height=540)
    
    
    cv2.imshow("Mask3", mask)
    
    key = cv2.waitKey(100000) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
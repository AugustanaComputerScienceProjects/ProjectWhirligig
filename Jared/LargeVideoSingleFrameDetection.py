# import the necessary packages
import numpy as np
import cv2
import imutils

def find_beetles_by_color(frame):
    # define the lower and upper boundaries of the 
    # whirligig beetles (using the HSV color space)
    lower_thresh_dark = np.array([10,10,10])
    upper_thresh_dark = np.array([50,35,50])
    
    lower_thresh_light = np.array([100,105,100])
    upper_thresh_light = np.array([200,200,200])
    
    
    

    # convert it to the HSV color space
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask based on hsv color range, then perform
    # a series of erode and dilations to remove any small
    # blobs left in the mask and merge small blogs into biggers ones
    mask_dark = cv2.inRange(frame, lower_thresh_dark, upper_thresh_dark)
    mask_light=cv2.inRange(frame, lower_thresh_light, upper_thresh_light)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    mask2 = cv2.erode(mask_dark, kernel, iterations=1)
    mask3 = cv2.dilate(mask2, kernel, iterations=6)
    
    edges = cv2.Canny(frame,50,100)
    cv2.imshow("edges", edges)
    
    # find contours in the mask 
    cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    coords = []
    improvedContourList = []

    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)          
        if 30 < radius <= 60:
            improvedContourList.extend(splitMultipleBeetles(mask3,c))
        else:
            improvedContourList.append(c)
          

    # process each contour in our contour list
    for c in improvedContourList:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if 10 < radius <= 30:
            coords.append((x,y))
            
                  #box = cv2.boxPoints(cv2.minAreaRect(c))
            #cv2.drawContours(frame,[np.int0(box)],0,(0,0,255),2)
            #cv2.circle(frame, (int(x), int(y)), int(radius),
                   # (0, 255, 255), 2)
    #mask3 = imutils.resize(mask3, width=1080, height=810)
    #cv2.imshow("Mask3", mask3)
    
    #mask_dark = imutils.resize(mask_dark, width=1080, height=810)
    #cv2.imshow("Mask Dark", mask_dark)
    
    #mask_light = imutils.resize(mask_light, width=1080, height=810)
    #cv2.imshow("Mask light", mask_light)
    return coords

def splitMultipleBeetles(maskImage, bigContour):
   x,y,w,h = cv2.boundingRect(bigContour)
   cropped = maskImage[y:(y + h),x:(x + w)]
   #kernel = np.ones((3,3),np.uint8)
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   eroded=cv2.erode(cropped, kernel, iterations=4)
   cnts = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
   for cnt in cnts:
       cnt += np.array([x,y])
   return cnts   
 

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
        frame = imutils.resize(frame, width=1080, height=810)
        cv2.imshow("Frame", frame)
        #cv2.imshow("Mask", mask)
        #cv2.imshow("Mask2", mask2)
       
        
        key = cv2.waitKey(1000000) & 0xFF
     
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
     
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
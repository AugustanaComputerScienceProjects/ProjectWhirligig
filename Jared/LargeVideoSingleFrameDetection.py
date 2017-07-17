# import the necessary packages
import numpy as np
import cv2
import imutils

def find_beetles_by_color(frame):
    # define the lower and upper boundaries of the 
    # whirligig beetles color
    
    #dark pixel color range on beetles
    lower_thresh_dark = np.array([10,10,10])
    upper_thresh_dark = np.array([50,35,50])
    
    #light pixel color range on beetles
    lower_thresh_light = np.array([100,105,100])
    upper_thresh_light = np.array([200,200,200])
    
    #mid pixel color range on beeles
    lower_thresh_mid = np.array([50,35,35])
    upper_thresh_mid = np.array([100,105,100])
    
    #Finds dark pixel color on beetle
    mask_dark = cv2.inRange(frame, lower_thresh_dark, upper_thresh_dark)
    
    #Finds lighter reflections on beetles
    mask_light=cv2.inRange(frame, lower_thresh_light, upper_thresh_light)
    
    #finds middle colors of beeltes which gives outline of beetle
    mask_mid=cv2.inRange(frame, lower_thresh_mid, upper_thresh_mid)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    mask2 = cv2.erode(mask_dark, kernel, iterations=1)
    mask3 = cv2.dilate(mask2, kernel, iterations=6)
    mask4=cv2.dilate(mask2, kernel, iterations=12)
    #cv2.imshow("mask4", mask4)
    combinedMask = cv2.bitwise_or(mask_dark,mask_light)
    edges = cv2.Canny(frame,25,75)
    combinedMask=cv2.bitwise_or(combinedMask,mask_mid)
    #cv2.imshow("combined", combined)
    combinedMask = cv2.bitwise_or(combinedMask, edges, mask=mask4)
    #cv2.imshow("combined2", combined2)
    closing = cv2.morphologyEx(combinedMask, cv2.MORPH_CLOSE, kernel, iterations=5)
    #cv2.imshow("closing", closing)
    # find contours in the mask 
    cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    coords = []
    improvedContourList = []

    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)          
        if 37 < radius <= 100:
            improvedContourList.extend(splitMultipleBeetles(mask3,c))
        else:
            improvedContourList.append(c)
          

    # process each contour in our contour list
    for c in improvedContourList:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if 10 < radius <= 37:
            coords.append((x,y))
            
                  #box = cv2.boxPoints(cv2.minAreaRect(c))
            #cv2.drawContours(frame,[np.int0(box)],0,(0,0,255),2)
            #cv2.circle(frame, (int(x), int(y)), int(radius),
                   # (0, 255, 255), 2)
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
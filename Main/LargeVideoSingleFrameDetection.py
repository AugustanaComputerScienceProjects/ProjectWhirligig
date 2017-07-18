# import the necessary packages
import numpy as np
import cv2
import imutils

def find_beetles_by_color(frame):
    # define the lower and upper boundaries of the 
    # whirligig beetles color
    
    lower_hsv_threshold = np.array([0,0,0])
    upper_hsv_threshold = np.array([200,200,80])
    
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
    mask3 = cv2.dilate(mask2, kernel, iterations=8)
    mask4=cv2.dilate(mask2, kernel, iterations=25)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    maskhsv = cv2.inRange(hsv, lower_hsv_threshold, upper_hsv_threshold)
    maskhsv2 = cv2.erode(maskhsv, None, iterations=1)
    maskhsv3 = cv2.dilate(maskhsv2, None, iterations=5)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(maskhsv3,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=8)
    
    cv2.imshow("sure_bg", sure_bg)
    combinedMask = cv2.bitwise_or(mask3,mask_light)
    edges = cv2.Canny(frame,25,75)
    combinedMask=cv2.bitwise_or(combinedMask,mask_mid)
    #cv2.imshow("combined", combined)
    combinedMask = cv2.bitwise_or(combinedMask, edges, mask=mask4)
    cv2.imshow("combinedMask", combinedMask)
    closing = cv2.morphologyEx(combinedMask, cv2.MORPH_CLOSE, kernel, iterations=5)
    cv2.imshow("closing", closing)
    # find contours in the mask 
    cnts = cv2.findContours(combinedMask.copy(), cv2.RETR_EXTERNAL,
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
   opening = cv2.morphologyEx(cropped,cv2.MORPH_OPEN,kernel, iterations = 2)

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
    
   #markers = cv2.watershed(frame,markers)
   #frame[markers == -1] = [255,0,0]
   


   cnts = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
   for cnt in cnts:
       #((x, y), radius) = cv2.minEnclosingCircle(cnt)
       #cv2.circle(frame, (int(x), int(y)), int(radius),
        #            (0, 255, 255), 2)
       cnt += np.array([x,y])
   return cnts   
 

CHECK_FRAME_LIST = [1] + list(range(151,178+1,3))
if __name__ == '__main__':
    frameFileName = r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4"
    # then initialize the
    # list of tracked points
    textFileName = frameFileName.replace('.mp4', '');
    
    
    camera = cv2.VideoCapture(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.mp4")
    frameNum = 0
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        frameNum += 1
        
        if not grabbed:
            break
 
        coords = find_beetles_by_color(frame)
        
        if frameNum in CHECK_FRAME_LIST:
            # process each contour in our contour list
            with open("%s_frame%04d_predicted.txt"%(textFileName,frameNum) , 'w') as fout:
                for x,y in coords:
                    fout.write(str(x) + ' ' + str(y) + '\n')

        for x,y in coords:
            cv2.circle(frame, (int (x), int (y)), 5, (0, 0, 255), -1)
                
        # show the frame to our screen
        frame = imutils.resize(frame, width=1080, height=810)
        cv2.imshow("Frame", frame)
       
        
        key = cv2.waitKey(1) & 0xFF
     
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
     
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
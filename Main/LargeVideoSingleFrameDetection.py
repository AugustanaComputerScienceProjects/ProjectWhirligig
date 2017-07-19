"""This program was made to analyze video large1.mp4 by looking at each frame 
and detecting all the beetles in that frame and their coordinates. However it 
does not find the identies of beetles. This program uses multiple masks looking 
for the different colors of the beetles. It also takes beetles that are too 
close together and splits them up so they are not tracked as one beetle"""

# import the necessary packages
import numpy as np
import cv2
import imutils

#Returns a list of the coordinates of the beetles
def find_beetles_by_color(frame):
    # define the lower and upper boundaries of the 
    # whirligig beetles color
    #looks for all red blue and dark green pixel color range on beetles
    lower_thresh_dark_green_green = np.array([0,0,0])
    upper_thresh_dark_green = np.array([255,37,255])
    
    #looks light pixel color range on beetles
    lower_thresh_light = np.array([100,105,100])
    upper_thresh_light = np.array([200,200,200])
    
    #looks for outline pixel color range on beeles and gives
    lower_thresh_outline = np.array([50,50,35])
    upper_thresh_outline = np.array([100,105,150])
    
    #looks for middle part of beetles
    #lower_thresh_mid = np.array([10,10,120])
    #upper_thresh_mid = np.array([250,250,250])
    #mask_mid = cv2.inRange(frame, lower_thresh_mid, upper_thresh_mid)
    #cv2.imshow("mask_mid", mask_mid)
    
    #Creates threshold mask that gives beetle shapes but picks up waves
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #Finds red blue and dark green pixel color on beetle
    mask_dark_green = cv2.inRange(frame, lower_thresh_dark_green_green, upper_thresh_dark_green)
    
    #Finds lighter reflections on beetles
    mask_light=cv2.inRange(frame, lower_thresh_light, upper_thresh_light)
   
    #finds middle colors of beeltes which gives outline of beetle
    mask_outline=cv2.inRange(frame, lower_thresh_outline, upper_thresh_outline)
    
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    mask_dark_green2 = cv2.morphologyEx(mask_dark_green,cv2.MORPH_OPEN,kernel, iterations = 1)
    #cv2.imshow("erode", mask2)
    mask_dark_green3 = cv2.dilate(mask_dark_green, kernel, iterations=5)
    mask_sure_beetles=cv2.dilate(mask_dark_green2, kernel, iterations=25)
    
    combinedMask = cv2.bitwise_or(mask_dark_green3,thresh)
    combinedMask= cv2.bitwise_or(combinedMask, mask_light)
    
    combinedMask=cv2.bitwise_or(combinedMask,mask_outline, mask=mask_sure_beetles)
    #cv2.imshow("combined", combined)
    #cv2.imshow("combinedMask", combinedMask)
    closing = cv2.morphologyEx(combinedMask, cv2.MORPH_CLOSE, kernel, iterations=5)
    closing = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel, iterations = 5)
    #cv2.imshow("closing", closing)
    # find contours in the mask 
    cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    coords = []
    improvedContourList = []

    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)          
        if 41 < radius <= 150:
            improvedContourList.extend(splitMultipleBeetles(frame,c))
        else:
            improvedContourList.append(c)
          

    # process each contour in our contour list
    for c in improvedContourList:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if 7 < radius <= 41:
            coords.append((x,y))
            

    #mask_dark_green=imutils.resize(mask_dark_green, width=1080, height=810)
    #cv2.imshow("Mask Dark", mask_dark_green)
    
    #mask_light=imutils.resize(mask_light, width=1080, height=810)
    #cv2.imshow("Mask Light", mask_light)
    
    mask_outline=imutils.resize(mask_outline, width=1080, height=810)
    cv2.imshow("Mask outline", mask_outline)
    return coords
    
def splitMultipleBeetles(frame, bigContour):
   x,y,w,h = cv2.boundingRect(bigContour)
   cropped = frame[y:(y + h),x:(x + w)]
   lower_thresh_mid = np.array([10,10,120])
   upper_thresh_mid = np.array([250,250,250])
   mask_mid = cv2.inRange(cropped, lower_thresh_mid, upper_thresh_mid)
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,1))
   dilated=cv2.erode(mask_mid, kernel, iterations=2)
   cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL,
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
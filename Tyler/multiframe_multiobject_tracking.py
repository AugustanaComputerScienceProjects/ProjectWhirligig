# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:56:07 2017

@author: tylermay14
"""


FONT = cv2.FONT_HERSHEY_SIMPLEX

trackers = cv2.MultiTracker("KCF");


# Read video
video = cv2.VideoCapture("S:/CLASS/CS/ProjectWhirligig/videos/large1.MP4")

successFlag, frame = video.read()

boxes= []

for i in range(5):
    boxes.append(cv2.selectROI(frame));


cv2.destroyAllWindows()

if (len(boxes) == 0):
    print("NO OBJECTS!")
    sys.exit(1)

trackers.add(frame,boxes)

while(True): 
    successFlag, frame = video.read()
    if not successFlag:
        cv2.waitKey(0)
        break 
    
    retVal, boxes = trackers.update(frame)
    for i, bbox in enumerate(boxes):
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,0,255))
        cv2.putText(frame,str(i),p1, FONT, 4,(255,255,255),2,cv2.LINE_AA)

    # Display result
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    if (cv2.waitKey(10) & 0xff) == 27:
        break
    

cv2.destroyAllWindows()
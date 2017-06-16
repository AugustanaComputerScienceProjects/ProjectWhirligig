import cv2
import numpy as np
from collections import deque
cap = cv2.VideoCapture(r"H:\Project Whiriligig\opencvtesting\medium2.mp4")

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while(1):
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    mask=cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)


    BUFFER_SIZE = 200
    pts = deque(maxlen=BUFFER_SIZE)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    #frame=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # process each contour in our contour list
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #M = cv2.moments(c)
        #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10 and radius < 20:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame2, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
            #cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
            # update the points queue
            pts.appendleft(center)

# loop over the set of tracked points
    for i in np.arange(0, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        #if pts[i - 1] is None or pts[i] is None:
        #    continue
 
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        #thickness = int(np.sqrt(BUFFER_SIZE / float(i + 1)) * 2.5)
        thickness = int(np.sqrt(BUFFER_SIZE - i) / 3 + 2)
        cv2.circle(frame2, pts[i], thickness, (0, 0, 255), -1)

        #cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    cv2.imshow('frame3', mask)
    cv2.imshow('frame2',rgb)
    cv2.imshow('frame1',frame2)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',frame2)
        cv2.imwrite('opticalhsv.png',rgb)
    prvs = next

cap.release()
cv2.destroyAllWindows()
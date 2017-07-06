import cv2
import numpy as np
from collections import deque
import imutils
import MediumVideoSingleFrameDetection as md
import LargeVideoSingleFrameDetection as ld
from MarkedvsTrackedAccuracyDetector import distanceSquared


class Beetle:
    """Represents one beetle's location in a video"""
    def __init__(self, ident, startX, startY):
        self.ident = ident
        self.x=startX
        self.y=startY
    def distanceToPoint(self, ptX, ptY):
        """computes the Euclidean distance to the given pt"""
        return ((self.x - ptX) ** 2 + (self.y - ptY) ** 2) ** 0.5
    def __str__(self):
        return "Beetle %s(%s,%s)"%(self.ident,self.x, self.y)
    def __repr__(self):
        return str(self)
#    def __eq__(self, other):
#        return self.ident == other.ident and self.x == other.x and self.y == other.y
    
def getFindingMethod(filename):
    if 'large' in filename:
        return ld.find_beetles_by_color
    elif 'medium' in filename:
        return md.find_beetles_combined
    else:
        raise Exception("I don't know what method to use for " + filename)
    
if __name__ == '__main__':
    filename="large1.mp4"
    cap = cv2.VideoCapture("H:\\Summer Research 2017\\Whirligig Beetle pictures and videos\\" + filename)
    
    successFlag, frame = cap.read()
    #successFlag, frame1 = cap.read()
    findingFunction = getFindingMethod(filename)
    prevLocations = findingFunction(frame)
    
    while(True): 
        successFlag, frame = cap.read()
        if not successFlag:
            cv2.waitKey(0)
            break 
        
        curLocations = findingFunction(frame)
        
        
        print ("Matched length:"+str(len(set(matched))))
        
        with open(textFileName, 'w') as fout:
            for x,y in set(matched):
            # draw a circle at each x,y that matched using cv2.circle
                cv2.circle(frame, (int (x),int (y)), 5, (0, 255, 255), -1)
                fout.write(str(x) + ' ' + str(y) + '\n')
    
        frame = imutils.resize(frame, width=1000, height=800)
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # esc key
            break
    cv2.destroyAllWindows()
    cap.release()
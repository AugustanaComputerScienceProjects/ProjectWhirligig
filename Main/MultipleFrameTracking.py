import cv2
import numpy as np
from collections import deque
import imutils
import MediumVideoSingleFrameDetection as md
import LargeVideoSingleFrameDetection as ld

from base36 import *

filename="large1.mp4"

TRACKING_COLOR_LIST = [(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),(128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),(66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),(255,255,0),(255,80,5)]

def distance(pt1, pt2):
    """computes the Euclidean distance between pts"""
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5

def distanceSquared(pt1, pt2):
    """computes the square of the Euclidean distance between pts"""
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

def intTuple(pt):
    return (int(pt[0]),int(pt[1]))


identCounter = 0

class Beetle:
    """Represents one beetle's location in a video"""
    def __init__(self, startFrame, startLoc):
        global identCounter
        self.ident = identCounter
        identCounter += 1
        self.frameNum = startFrame
        self.loc=startLoc
        self.history=[(startFrame-1,startLoc) ]
    def __str__(self):
        return "Beetle %s {Frame %s: %s hist=%s}"%(self.ident,self.frameNum,self.loc,self.history)
    def __repr__(self):
        return str(self)
    def updateCoord(self, frameNum, newLoc):
        self.history.append((self.frameNum,self.loc))
        self.frameNum = frameNum
        self.loc = newLoc
    def getLastFrameSeen(self):
        return self.frameNum
    def getTrackingColor(self):
        return TRACKING_COLOR_LIST[self.ident % len(TRACKING_COLOR_LIST)]
    def getCurrentLoc(self):
        return self.loc
    def predictNewLocUsingCurrentLoc(self,futureFrameNum):
        return self.loc
    def predictNewLocUsingVelocity(self,futureFrameNum):
        frameDiff = self.frameNum - self.history[-1][0]
        curX,curY = self.loc
        oldX,oldY = self.history[-1][1]
        velX = (curX - oldX) / frameDiff
        velY = (curY - oldY) / frameDiff
        timePassed = futureFrameNum-self.frameNum
        return (curX + velX*timePassed, curY + velY*timePassed)
        
        
#    def __eq__(self, other):
#        return self.ident == other.ident and self.x == other.x and self.y == other.y
    
def getFindingMethod(filename):
    if 'large' in filename:
        return ld.find_beetles_by_color
    elif 'medium' in filename:
        return md.find_beetles_combined
    else:
        raise Exception("I don't know what method to use for " + filename)

def getMovementBetweenFramesThreshold(filename):
    if 'large' in filename:
        return 30
    elif 'medium2' in filename:
        return 6.3
    elif 'medium5' in filename:
        return 8.2
    else:
        raise Exception("I don't know what method to use for " + filename)

    
if __name__ == '__main__':
    
    cap = cv2.VideoCapture("H:\ProjectWhirligig\\" + filename)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter("MultipleFrameTracking.avi", fourcc, 20.0, (1080, 810))
    
    if filename == 'large1.mp4':
        for i in range(5*30): # Note not actually 30 FPS!
            successFlag, frame = cap.read()
    
    successFlag, frame = cap.read()
    #successFlag, frame1 = cap.read()
    findingFunction = getFindingMethod(filename)
    curLocations = findingFunction(frame)
    
    activeBeetleList = []
    archivedBeetleList = []
    beetlesWithLongHistories = set([])
    
    frameNum = 0
    for loc in curLocations:
        activeBeetleList.append(Beetle(frameNum,loc))
    
    while(True): 
        successFlag, frame = cap.read()
        frameNum += 1
        if not successFlag:
            cv2.waitKey(0)
            break 
        
        curLocations = set(findingFunction(frame))
        cv2.putText(frame, " " + str(frameNum), (0,1040), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
        newActiveBeetleList = []
        for beetle in activeBeetleList:
            if len(curLocations) > 0:
                beetleLoc= beetle.getCurrentLoc() # OR velocity predicted?
                #find closest to last frame
                #bestLoc = min(curLocations, key=lambda pt: distanceSquared(beetleLoc,pt))
                #find closest based on velocity
                bestLoc = min(curLocations, key=lambda pt: distanceSquared(beetle.predictNewLocUsingVelocity(frameNum), pt))
                if distance(bestLoc,beetleLoc) < getMovementBetweenFramesThreshold(filename):
                    curLocations.remove(bestLoc)
                    beetle.updateCoord(frameNum,bestLoc)
                    #cv2.circle(frame, (int (x),int (y)), 5, (0, 255, 255), -1)
                    color = beetle.getTrackingColor()
                    cv2.arrowedLine(frame,intTuple(beetle.history[-1][1]), intTuple(beetle.getCurrentLoc()), color, 2, 0, 0, 0.5)
                    cv2.putText(frame, " " + base36encode(beetle.ident), intTuple(beetle.loc), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            if frameNum - beetle.getLastFrameSeen() > 5: #lost for 5 consecutive frames
                # TODO: remove short history beetles here for efficiency, instead of filtering them out later?
                archivedBeetleList.append(beetle)      
            else:
                newActiveBeetleList.append(beetle)
            
            if len(beetle.history) > 200 and beetle not in beetlesWithLongHistories:
                beetlesWithLongHistories.add(beetle)
                print("# with long histories: %s"%len(beetlesWithLongHistories))

        # add new beetles for each detected blob in the current frame that wasn't matched to a beetle
        for newPt in curLocations:
            newActiveBeetleList.append(Beetle(frameNum,newPt))
            cv2.circle(frame, intTuple(newPt), 4, (0, 255, 255), -1)
            
        activeBeetleList = newActiveBeetleList
        
    
        #frame = imutils.resize(frame, width=1200, height=900)
        frame = imutils.resize(frame, width=1080, height=810)
        cv2.imshow("Frame", frame)
        out.write(frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # esc key
            break
    cv2.destroyAllWindows()
    cap.release()
    out.release()
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 11:02:32 2017

@author: jaredhaeme15
"""

def matches(xm, ym, xt, yt):
    return ((xt-15) <= xm <= (xt+15)) and yt-15 <= ym <= yt+15

with open(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1.txt") as f:
    videoTrackedCoord = [tuple(map(float, i.split(' '))) for i in f]
videoTrackedCoordNum=len(videoTrackedCoord)
#print (videoTrackedCoord)
print ("Number of beetles in Tracked video frame:"+ str(len(videoTrackedCoord)))

with open(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\marked_frames\large1_frame0001_markedJH.txt") as f:
    markedCoord = [tuple(map(float, i.split(' '))) for i in f]
markedCoordNum=len(markedCoord)
#print ('\n', markedCoord)
print ("Number of beetles in marked image:"+ str(markedCoordNum))

groupTrackedasOne=0
markedMatched=[]
trackedMatched=[]
sameBugTrackedMoreThanOnce=0
matched = 0
for xm, ym in markedCoord:
    for xt, yt in videoTrackedCoord:
        if matches(xm, ym, xt, yt):
            matched+=1
            markedMatched.append((xm,ym))
            trackedMatched.append((xt, yt))
            
for pt in markedMatched:
    if markedMatched.count(pt)>1:
        sameBugTrackedMoreThanOnce+=1

for pt in trackedMatched:
    if trackedMatched.count(pt)>1:
        groupTrackedasOne+=1

markedNotMatched=list(set(markedCoord) - set(markedMatched))
trackedMatchedNotMatched=list(set(videoTrackedCoord) - set(trackedMatched))
falseNeg=len(markedNotMatched)
falsePos=len(trackedMatchedNotMatched)

accuracy=((markedCoordNum-(falsePos+falseNeg+sameBugTrackedMoreThanOnce+groupTrackedasOne))/markedCoordNum)*100
print ("Matched beetles:"+str(matched))
print ("False positives:"+str(falsePos))
print ("False negatives:"+str(falseNeg))
print ("Bug Tracked more than once:"+str(sameBugTrackedMoreThanOnce))
print ("Group of bugs tracked as one:"+str(groupTrackedasOne))
print ("Accuracy:"+str('{0:.4g}'.format(accuracy)+"%"))


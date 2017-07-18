import matplotlib.pyplot as plt

def matches(xm, ym, xt, yt, boxRadius):
    return ((xt-boxRadius) <= xm <= (xt+boxRadius)) and yt-boxRadius <= ym <= yt+boxRadius

def distanceSquared(pt1, pt2):
    x1,y1=pt1
    x2,y2=pt2
    return (x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)


    
def compareMarkedAndTrackedFrames(trackedCoordFile, markedCoordFile, 
                                  frameImageFile, boxRadius):
    with open(trackedCoordFile) as f:
        videoTrackedCoord = [tuple(map(float, i.split(' '))) for i in f]
    videoTrackedCoordNum=len(videoTrackedCoord)
    #print (videoTrackedCoord)
    print ("Number of beetles in Tracked video frame:"+ str(len(videoTrackedCoord)))
    
    with open(markedCoordFile) as f:
        markedCoord = [tuple(map(float, i.split(' '))) for i in f]
    markedCoordNum=len(markedCoord)
    #print ('\n', markedCoord)
    print ("Number of beetles in marked image:"+ str(markedCoordNum))
    
    groupTrackedasOne=0
    markedMatched=[]
    trackedMatched=[]
    sameBugTrackedMoreThanOnce=0
    matched = 0
    bestMatches = []
    for xm, ym in markedCoord:
        potentialBestMatches = []
        for xt, yt in videoTrackedCoord:
            if matches(xm, ym, xt, yt, boxRadius):
                matched+=1
                markedMatched.append((xm,ym))
                trackedMatched.append((xt, yt))
                potentialBestMatches.append((xt,yt))
        
        if len(potentialBestMatches) > 0:
            # code to find the NEAREST potential match (xt,yt) to xm,ym
            (xt,yt) = min(potentialBestMatches, key=lambda pt: distanceSquared(pt,(xm,ym)))
            bestMatches.append((xm,ym,xt,yt))


    bugsTrackedMultiple = []
    for pt in markedMatched:
        if markedMatched.count(pt)>1:
            sameBugTrackedMoreThanOnce+=1
            bugsTrackedMultiple.append(pt)
    
    print("btm: ", bugsTrackedMultiple)
    print("set:", set(bugsTrackedMultiple))
    
    bugsTrackedasOne=[]
    for pt in trackedMatched:
        if trackedMatched.count(pt)>1:
            groupTrackedasOne+=1
            bugsTrackedasOne.append(pt)
            
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
    
    im = plt.imread(frameImageFile)
    plt.figure(figsize=(10.5,7))
    implot = plt.imshow(im, aspect='auto')
    plt.scatter(*zip(*videoTrackedCoord), c='y', s=5)
    plt.scatter(*zip(*markedCoord), c='r', marker='x', s=5)
    for xm,ym,xt,yt in bestMatches:
        plt.plot([xm,xt],[ym,yt], 'g-')
    
    for x,y in set(bugsTrackedMultiple):
        plt.scatter([x],[y], c='m', marker='v')
    
    plt.show()

CHECK_FRAME_LIST = [1] + list(range(151,178+1,3))

for frameNum in CHECK_FRAME_LIST:
    compareMarkedAndTrackedFrames(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1_frame%04d_predicted.txt"%frameNum,
                                  r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1_frame%04d.txt"%frameNum,
                                  r"H:/Summer Research 2017/Whirligig Beetle pictures and videos/large1_frame%04d.png"%frameNum,
                                  15)

#compareMarkedAndTrackedFrames(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5.txt",
#                              r"H:\Summer Research 2017\ProjectWhirligig\Jared\medium5_frame0001_markedHH.txt",
#                              r"H:/Summer Research 2017/Whirligig Beetle pictures and videos/medium5_frame0001.png",
#                              6)

#compareMarkedAndTrackedFrames(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5MultipleMethods.txt",
#                              r"H:\Summer Research 2017\ProjectWhirligig\Jared\medium5_frame0001_markedHH.txt",
#                              r"H:/Summer Research 2017/Whirligig Beetle pictures and videos/medium5_frame0001.png",
#                              6)

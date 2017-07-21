"""This program compares the manually humaned marked frames of beetles videos and 
compares them to the single frame tracking programs to test the accuracy of the
tracking programs. This program takes in text files of coordinates and checks to see
if the tracked cordintes of the computer are within a certain distance of the 
human marked coordinates"""

import matplotlib.pyplot as plt

#checks if two points match together if they are withing a certain distance of each
#other
def matches(xm, ym, xt, yt, boxRadius):
    return ((xt-boxRadius) <= xm <= (xt+boxRadius)) and yt-boxRadius <= ym <= yt+boxRadius

#finds the squared distance between two points
def distanceSquared(pt1, pt2):
    x1,y1=pt1
    x2,y2=pt2
    return (x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)


    
def compareMarkedAndTrackedFrames(trackedCoordFile, markedCoordFile, 
                                  frameImageFile, boxRadius):
    #Reads in computer tracked coordinates text file
    with open(trackedCoordFile) as f:
        videoTrackedCoord = [tuple(map(float, i.split(' '))) for i in f]
    videoTrackedCoordNum=len(videoTrackedCoord)
    #print (videoTrackedCoord)
    print ("Number of beetles in Tracked video frame:"+ str(len(videoTrackedCoord)))
    
    #Reads in marked coordinates text file
    with open(markedCoordFile) as f:
        markedCoord = [tuple(map(float, i.split(' '))) for i in f]
    markedCoordNum=len(markedCoord)
    #print ('\n', markedCoord)
    print ("Number of beetles in marked image:"+ str(markedCoordNum))
    
    
    markedMatched=[]
    trackedMatched=[]
    bestMatches = []
    matched = 0
    groupTrackedasOne=0
    sameBugTrackedMoreThanOnce=0
    
    #loops through list of marked coordinates
    for xm, ym in markedCoord:
        potentialBestMatches = []
        #loops through list of tracked coordinates
        for xt, yt in videoTrackedCoord:
            #checks if coordinates of tracked beetles are within a certain range 
            #of the marked beetles
            if matches(xm, ym, xt, yt, boxRadius):
                matched+=1
                #Adds to list of all marked coordinates that 
                #matched to a tracked coordinate
                markedMatched.append((xm,ym))
                #Adds to list of all tracked coordiantes that matched to 
                #the marked coordiantes
                trackedMatched.append((xt, yt))
                #Adds to list of all tracked matches to later find the best mathces
                potentialBestMatches.append((xt,yt))
        
        if len(potentialBestMatches) > 0:
            # code to find the NEAREST potential match (xt,yt) to xm,ym
            (xt,yt) = min(potentialBestMatches, key=lambda pt: distanceSquared(pt,(xm,ym)))
            #Adds to list of closest point in case two tracked points were in the range
            #or two marked point in range of tracked point so that there is one to one matching
            bestMatches.append((xm,ym,xt,yt))

    #Looks for duplicates in the marked matched list to see
    #if same bug matched to two or more tracked points
    bugsTrackedMultiple = []
    for pt in markedMatched:
        if markedMatched.count(pt)>1:
            sameBugTrackedMoreThanOnce+=1
            bugsTrackedMultiple.append(pt)
    
    print("btm: ", bugsTrackedMultiple)
    print("set:", set(bugsTrackedMultiple))
    
    #Looks for duplicates in tracked list to see if tracked point matched to
    #multiple marked points
    bugsTrackedasOne=[]
    for pt in trackedMatched:
        if trackedMatched.count(pt)>1:
            groupTrackedasOne+=1
            bugsTrackedasOne.append(pt)
    
    #Calculates all the erros in the tracking        
    markedNotMatched=list(set(markedCoord) - set(markedMatched))
    trackedMatchedNotMatched=list(set(videoTrackedCoord) - set(trackedMatched))
    falseNeg=len(markedNotMatched)
    falsePos=len(trackedMatchedNotMatched)
    #Takes all the marked coordinates subtracts all the errors and divides 
    #by the marked coordinates to calculate the accuracy
    accuracy=((markedCoordNum-(falsePos+falseNeg+sameBugTrackedMoreThanOnce+groupTrackedasOne))/markedCoordNum)*100
    print ("Matched beetles:"+str(matched))
    print ("False positives:"+str(falsePos))
    print ("False negatives:"+str(falseNeg))
    print ("Bug Tracked more than once:"+str(sameBugTrackedMoreThanOnce))
    print ("Group of bugs tracked as one:"+str(groupTrackedasOne))
    print ("Accuracy:"+str('{0:.4g}'.format(accuracy)+"%"))
    
    #Plots out picture with points. Red points are marked yellow are tracked
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
    return accuracy

#List of frames that were marked
CHECK_FRAME_LIST =list(range(151,178+1,3))
#Used to calculate overall accuracy
num=0
total=0
#for frameNum in CHECK_FRAME_LIST:
#    num+=1
#    print(num)
#    total+=compareMarkedAndTrackedFrames(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1_frame%04d_predicted.txt"%frameNum,
#                                  r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\large1_frame%04d.txt"%frameNum,
#                                  r"H:/Summer Research 2017/Whirligig Beetle pictures and videos/large1_frame%04d.png"%frameNum,
#                                  15)
#print ("Overall accuracy:"+str(str('{0:.4g}'.format(total/num)+"%")))
for frameNum in CHECK_FRAME_LIST:
    num+=1
    print(num)
    total+=compareMarkedAndTrackedFrames(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5_frame%04d_predicted.txt"%frameNum,
                                  r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5_frame%04d.txt"%frameNum,
                                  r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5_frame%04d.png"%frameNum,
                                  6)
print ("Overall accuracy:"+str(str('{0:.4g}'.format(total/num)+"%")))
#compareMarkedAndTrackedFrames(r"H:\Summer Research 2017\Whirligig Beetle pictures and videos\medium5MultipleMethods.txt",
#                              r"H:\Summer Research 2017\ProjectWhirligig\Jared\medium5_frame0001_markedHH.txt",
#                              r"H:/Summer Research 2017/Whirligig Beetle pictures and videos/medium5_frame0001.png",
#                              6)

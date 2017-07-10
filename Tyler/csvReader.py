# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pylab import *
import csv
with open('H:/ProjectWhirligig/whirligigSimulationExperiment-table.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    xCoords = []
    yCoords = []
    beetleList = [[]]
    for i in range(100):
        beetleList.append([])
    count = 0
    index = 0
    for row in reader:
        count = count + 1
        if(count >= 8):
            xCoords = row[9][1:-1].split(' ')
            for i in range (len(xCoords)):
                xCoords[i] = float(xCoords[i])
 
            yCoords = row[10][1:-1].split(' ')
            for i in range (len(yCoords)):
                yCoords[i] = float(yCoords[i])
            for i in range (len(xCoords)):
                beetleList[index].append((xCoords[i], yCoords[i]))
            index+=1
    newList = list(zip(*beetleList))
    for i in range(100):
        beetlexs, beetleys = zip(*newList[i])
        plot(beetlexs, beetleys)




             

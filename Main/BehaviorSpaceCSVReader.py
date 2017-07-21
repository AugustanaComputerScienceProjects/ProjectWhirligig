# -*- coding: utf-8 -*-
"""
@author: tylermay14

Takes NetLogo behavior space csv data and extracts the x and y locations of each beetle at each tick.  
The path of each beetle is plotted.
"""
from pylab import *
import csv
with open('H:/Summer Research 2017/ProjectWhirligig/whirligigSimulationExperiment-table.csv', newline='') as csvfile:
    for i in range(7):      #skip header lines
        csvfile.readline()
    reader = csv.reader(csvfile)
    xCoords = []
    yCoords = []
    beetleList = []

    for row in reader:
        beetleList.append([])
        xCoords = row[8][1:-1].split(' ')
        for i in range (len(xCoords)):
            xCoords[i] = float(xCoords[i])
 
        yCoords = row[9][1:-1].split(' ')
        for i in range (len(yCoords)):
            yCoords[i] = float(yCoords[i])
        for i in range (len(xCoords)):
            beetleList[-1].append((xCoords[i], yCoords[i]))

    newList = list(zip(*beetleList))
    for i in range(len(newList)):
        beetlexs, beetleys = zip(*newList[i])
        plot(beetlexs, beetleys)




             

# -*- coding: cp936 -*-
import os
import datetime
import math
# from DayTotalRadiance import LevAstRad
# from test import GetCoeffab
# from test import GetCoeffAB
# from test import GetLL
from LevCalRad import LevAstRad
from InOrNot import HaveORNot
from CalCvDegree import CVA
import numpy
import arcpy


SunPara = 1366.7
PI = math.pi
PI180 = math.pi / 180.0
SunPara = 1366.7
NDirect = 14
DataDistance = 1.0
DataTime = 5.0
DataTime = DataTime*(PI/ 720)
TD = 15.0 * PI180
Resolution = 1.0




#x = [1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1]
#Nx = len(x)
#xx = [1,3,4,5,6,7,9,10,11,12,13,14,15,16,17]
def TimeAngleBE(x, Nx):
    #print x
    #print Nx
    m = 0
    xx = [0 for i in range(Nx)]
    w1 = [0 for i in range(Nx)]
    w2 = [0 for i in range(Nx)]
    #print x
    for i in range(0, Nx):
        if x[i] > 0.25:
            xx[m] = i+1
            m = m + 1
    iNumberXX = m
    #print xx
    if iNumberXX == 0.0:
        LNumber = 1
        w1[0] = 1.0
        w2[0] = 1.0
    else:
        n = 1
        #w1[0] = xx[0]
        for i in range(1,iNumberXX):
            if xx[i] == xx[i-1] + 1.0:
                w1[n-1] = xx[i-1]
                w2[n-1] = xx[i]
                n = n + 1
        #w2[n-1] = xx[iNumberXX-1]
        LNumber = n
        #print w1, w2
        #LNumber = 0
        #for i in range(0,iNumberXX-1):
            #jiange = w2[i]-w1[i]
            #LNumber = LNumber + jiange
    return (w1,w2,LNumber)


#w1,w2,LNumber = TimeAngleBE(x,Nx)
#print w1,w2,LNumber
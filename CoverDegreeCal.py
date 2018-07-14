# -*- coding: cp936 -*-
import os
import datetime
import math
# from DayTotalRadiance import LevAstRad
# from test import GetCoeffab
# from test import GetCoeffAB
# from test import GetLL
import numpy
#from osgeo import gdal
import arcpy

SunPara = 1366.7
PI = math.pi
PI180 = math.pi / 180.0
SunPara = 1366.7
NDirectAngle = 72
Resolution = 1000.0
CVDatadistance = 1000.0
CVDirect = [0 for i in range(NDirectAngle)]
for k in range(0,NDirectAngle):
    CVDirect[k] = k*360.0/NDirectAngle*PI180
def CoverDegree(ix, iy, Altitude, sNumRow, sNumColumn):
    CVvalue = 0.0
    for i in range(0,NDirectAngle):
        CVDirectValue = 0.0
        for j in range(1,10):
            RDistance = j * CVDatadistance
            DataX = RDistance * math.sin(CVDirect[i])
            DataX = abs(DataX) - Resolution / 2.0
            if math.sin(CVDirect[i]) <= 0.0:
                if DataX <= 0.0:
                    NyStation = iy
                else:
                    NxDirect = int(DataX / Resolution) + 1
                    NyStation = iy - NxDirect
            else:
                if DataX <= 0.0:
                    NyStation = iy
                else:
                    NxDirect = int(DataX / Resolution) + 1
                    NyStation = iy + NxDirect
            DataY = RDistance * math.cos(CVDirect[i])
            DataY = abs(DataY) - Resolution / 2.0
            if math.cos(CVDirect[i]) <= 0.0:
                if DataY <= 0.0:
                    NxStation = ix
                else:
                    NyDirect = int(DataY/Resolution) + 1
                    NxStation = ix - NyDirect
            else:
                if DataY <= 0.0:
                    NxStation = ix
                else:
                    NyDirect = int(DataY / Resolution) + 1
                    NxStation = ix + NyDirect
            NxStation = max(0, min(NxStation, sNumRow - 1))
            NyStation = max(0, min(NyStation, sNumColumn - 1))
            #print Altitude[ix][iy], Altitude[NxStation][NyStation]
            TanSlope = (int(Altitude[NxStation][NyStation]) - int(Altitude[ix][iy]))/RDistance
            if TanSlope > CVDirectValue:
                CVDirectValue = TanSlope
        Alpha = math.atan(CVDirectValue)
        # P点在某方位下的地形开阔度，1-sin(alpha)
        CVDirectValue = 1.0 - math.sin(Alpha)
        #计算2pi内各方位开阔度，累加求平均
        CVvalue = CVvalue + CVDirectValue

    CVvalue = CVvalue / NDirectAngle
    #print CVvalue
    return CVvalue


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
NDirect = 14
DataDistance = 1000.0
DataTime = 5.0
DataTime = DataTime*(PI/720)
TD = 15.0 * PI180
Resolution = 1000.0

def HaveORNot(row,column,sLat, Alt, sNumRow, sNumColumn, Declination, TAngle):
    #DataDistance = 1000
    #sLat = PI * sLat / 180
    sinH = math.sin(sLat) * math.sin(Declination) + math.cos(sLat) * math.cos(Declination) * math.cos(TAngle)
    if sinH <= 0.0:
        sinH = 0.0
    cosH = math.sqrt(1.0 - math.pow(sinH, 2))
    TanH = sinH/cosH
    sinA = math.cos(Declination) * math.sin(TAngle)/cosH
    #print sinA
    if sinA >= 1.0:
        sinA = 1.0
    if sinA <= -1.0:
        sinA = -1.0
    cosA = (sinH * math.sin(sLat) - math.sin(Declination))/cosH/math.cos(sLat)
    sHN = 1
    for k in range(1, 3):
        RDistance = k * DataDistance
        DataX = RDistance * sinA
        DataX = abs(DataX) - Resolution/2.0
        #print DataX
        if DataX <= 0.0:
            NyStation = column
        else:
            Nxdirect = int(DataX/Resolution) + 1
            if sinA <= 0.0:
                NyStation = column - Nxdirect
            else:
                NyStation = column + Nxdirect
        DataY = RDistance * cosA
        DataY = abs(DataY) - Resolution / 2.0
        #print DataY
        if DataY <= 0.0:
            NxStation = row
        else:
            Nydirect = int(DataY/Resolution) + 1
            if cosA <= 0.0:
                NxStation = row - Nydirect
            else:
                NxStation = row + Nydirect
        NxStation = max(0, min(NxStation, sNumRow-1))
        NyStation = max(0, min(NyStation, sNumColumn-1))
        #print NxStation,NyStation,ii,jj
        HH = int(Alt[NxStation][NyStation]) - int(Alt[row][column])
        #print Alt[NxStation][NyStation],Alt[row][column]
        #print HH
        TanSlope = HH/RDistance
        #print TanSlope
        if TanSlope > TanH:
            sHN = 0
            #print k
            break
    #print sHN
    return sHN




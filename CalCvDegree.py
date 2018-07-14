# -*- coding: cp936 -*-


import os
import datetime
import math
# from DayTotalRadiance import LevAstRad
# from test import GetCoeffab
# from test import GetCoeffAB
# from test import GetLL
from LevCalRad import LevAstRad
import numpy
#from osgeo import gdal
import arcpy


SunPara = 1366.7
PI = math.pi
PI180 = PI/180.0
SunPara = 1366.7
NDirect = 14
DataDistance = 1.0
DataTime = 5.0
DataTime = DataTime*(PI/ 720)
TD = 15.0 * PI180
Resolution = 1.0


def CVA(N, D, X, JULDAY, sLat, sSlope, sAspect,Declination):
    #print sAspect
    Aspect = sAspect*PI180
    #print Aspect
    Slope = sSlope

    W0 = 12.0 + X/TD
    if Aspect < PI / 2:
        # Northeast
        ISP = 1
    elif Aspect >= PI / 2 and Aspect <= PI:
        ISP = 2
        # southeast
        Aspect = PI - Aspect
    elif Aspect > PI and Aspect <= 1.5 * PI:
        ISP = 3
        # southwest
        Aspect = Aspect - PI
    else:
        ISP = 4
        # Northwest
        Aspect = 2 * PI - Aspect
    iSun = [0 for i in range(N)]
    for i in range(0, N):
        XU = W0 + i * D
        W = 15 * (XU - 12) * PI180
        sinH = math.sin(sLat) * math.sin(Declination) + math.cos(sLat) * math.cos(Declination) * math.cos(W)
        H = max(0.0, math.asin(sinH))
        cosH = math.cos(math.asin(sinH))
        cosB = (sinH * math.sin(sLat) - math.sin(Declination))/cosH/math.cos(sLat)
        cosB = max(-1.0, min(1.0, cosB))
        Alpha = math.acos(cosB)
        S1 = 0.0
        if ISP == 1:
            if XU < 12.0:
                if Alpha >= PI / 2 - Aspect:
                    Beta = 0.0
                else:
                    S1 = PI / 2 - Alpha - Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            else:
                if Alpha >= PI / 2 + Aspect:
                    Beta = 0.0
                else:
                    S1 = PI / 2 - Alpha + Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
        # southeast
        elif ISP == 2:
            # morning
            if XU < 12.0:
                if Alpha <= PI / 2 + Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI / 2 - Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            # afternoon
            else:
                if Alpha <= PI / 2 - Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI / 2 + Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
        elif ISP == 3:
            # morning
            if XU < 12.0:
                if Alpha <= PI / 2 - Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI / 2 + Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            # afternoon
            else:
                if Alpha <= PI / 2 + Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI / 2 - Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
        elif ISP == 4:
            # morning
            if XU < 12.0:
                if Alpha <= PI / 2 + Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI / 2 + Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            # afternoon
            else:
                if Alpha <= PI / 2 - Aspect:
                    Beta = 0.0
                else:
                    S1 = PI / 2 - Alpha - Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
    #print iSun

    return iSun
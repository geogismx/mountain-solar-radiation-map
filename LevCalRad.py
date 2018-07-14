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
# NDirectAngle = 8
NDirect = 14
DataDistance = 1.0
DataTime = 5.0
DataTime = DataTime*(PI/ 720)
TD = 15.0 * PI180
Resolution = 1.0

def LevAstRad(sLat, jd):
    Declination = 0.0
    JulDAY = jd
    DayA = 2 * PI * (JulDAY - 1) / 365.2422
    #sLat = PI * sLat / 180
    Declination = 0.4102 * math.sin(2 * PI * (JulDAY - 80) / 365.0)
    # Declination = 0.006894-0.399512*math.cos(DayA)+0.072075*math.sin(DayA)-0.006799*math.cos(2*DayA)+0.000896*math.sin(2*DayA)-0.002689*math.cos(3*DayA)+0.001516*math.sin(3*DayA)
    coshaf = 0.0 - math.tan(sLat) * math.tan(Declination)
    if coshaf >= 1.0:
        TAss = PI
    else:
        TAss = math.acos(coshaf)
    DayL = 2.0 * TAss / 0.261799
    E0 = 1.000109 + 0.033494 * math.cos(DayA) + 0.001472 * math.sin(DayA) + 0.000768 * math.cos(
        2.0 * DayA) + 0.000079 * math.sin(2.0 * DayA)
    ARad = SunPara * E0 * (24.0 * 3600.0) / PI * (TAss * math.sin(sLat) * math.sin(Declination) + math.cos(sLat) * math.cos(Declination) * math.sin(TAss))
    ARad = ARad / 1000000.0
    return (DayL, ARad, TAss, E0,Declination)

# F = open(r"C:\Users\George\Desktop\solar radiation\57131.txt",'rb')
# W = open(r"C:\Users\George\Desktop\temp.txt",'w')
# def getDayLofYear(sLat):
#     lines = F.readlines()
#     for i in range(0,len(lines)):
#         sline = lines[i].split("    ")
#         array = filter(None, sline)
#         #print array
#         Year = array[1].strip()
#         Month = array[2].strip()
#         Day = array[3].strip()
#         fmt = '%Y.%m.%d'
#         s = Year + '.' + Month + '.' + Day
#         JD = datetime.datetime.strptime(s, fmt).timetuple().tm_yday
#         Duration = array[4].strip()
#         WRT = LevAstRad(sLat,JD)
#         DayL = WRT[0]
#         ARad = WRT[1]
#         W.writelines(str(Year)+','+str(JD)+ ','+str(Duration)+','+str(DayL)+','+str(ARad)+'\n')
#     return 0
# sLat = PI * 34.43/180
# dic1 = getDayLofYear(sLat)
# print dic1

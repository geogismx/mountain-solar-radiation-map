

import os
import datetime
import math
#from DayTotalRadiance import LevAstRad
#from test import GetCoeffab
#from test import GetCoeffAB
#from test import GetLL
import numpy as np
from osgeo import gdal

SunPara = 1366.7
PI = math.pi
PI180 = math.pi/180.0
SunPara = 1366.7
#NDirectAngle = 8
NDirect = 14
DataDistance = 1000.0
DataTime = 5.0
DataTime = DataTime*(math.pi/720)
TD = 15.0*PI180
Resolution = 1000.0

TimeAngle = []
sWtimeHN = []

outputresult = "C:\Users\George\Desktop\pythontest\output.txt"

idw = "C:/Users/George/Desktop/pythontest/testgeo/20081.tif"
s1 = idw.index("2008")
s2 = idw.index(".tif")
ss = idw[s1+4:s2]
print ss

in_idw = gdal.Open(idw)
idw_band = in_idw.GetRasterBand(1)
sNumRow = idw_band.XSize
sNumColumn = idw_band.YSize

os.chdir("D:\idw")
in_slope = gdal.Open("slope.tif")
in_aspect = gdal.Open("aspect.tif")
in_xy = gdal.Open("latlong.tif")
xy_band = in_xy.GetRasterBand(1)
slope_band = in_slope.GetRasterBand(1)
aspect_band = in_aspect.GetRasterBand(1)
Slope = slope_band.ReadAsArray()
Aspect = aspect_band.ReadAsArray()
Altitude = xy_band.ReadAsArray()
print Slope[153][142]
gt = in_xy.GetGeoTransform()
print xy_band.YSize
print gt[0], gt[3], gt[0] + gt[1] * idw_band.XSize,gt[3] + gt[5] * idw_band.YSize
print gt[0], gt[3], gt[0] + gt[1] * xy_band.XSize,gt[3] + gt[5] * xy_band.YSize
#print sNumRow
#print sNumColumn
Latitude = []
def LevAstRad(sLat,jd):
    JulDAY = jd
    DayA = 2*PI*(JulDAY-1)/365.2422
    sLat = PI*sLat/180
    Declination = 0.4102*math.sin(2*PI*(JulDAY-80)/365.0)
    #Declination = 0.006894-0.399512*math.cos(DayA)+0.072075*math.sin(DayA)-0.006799*math.cos(2*DayA)+0.000896*math.sin(2*DayA)-0.002689*math.cos(3*DayA)+0.001516*math.sin(3*DayA)
    coshaf = 0.0 - math.tan(sLat)*math.tan(Declination)
    if coshaf >= 1.0:
        TAss = PI
    else:
        TAss = math.acos(coshaf)   
    DayL = 2.0*TAss/0.261799
    E0 = 1.000109+0.033494*math.cos(DayA)+0.001472*math.sin(DayA)+0.000768*math.cos(2.0*DayA)+0.000079*math.sin(2.0*DayA)
    ARad = SunPara*E0*(24.0*3600.0)/PI*(TAss*math.sin(sLat)*math.sin(Declination)+math.cos(sLat)*math.cos(Declination)*math.sin(TAss))
    ARad = ARad/1000000.0
    return (Declination,DayL,ARad,TAss,E0)

def HaveORNot(i,j,sLat,Alt,sNumRow,sNumColumn,Declination,TAngle):
    DataDistance = 1000.0
    sinH = math.sin(sLat) * math.sin(Declination) + math.cos(sLat) * math.cos(Declination) * math.cos(TAngle)
    if sinH <= 0.0:
        sinH = 0.0
    cosH = math.sqrt(1.0 - math.pow(sinH,2))
    TanH = sinH/cosH
    sinA = math.cos(Declination) * math.sin(TAngle)/cosH
    if sinA >= 1.0:
        sinA = 1.0
    if sinA <= -1.0:
        sinA = -1.0
    cosA = (sinH * math.sin(sLat) - math.sin(Declination))/cosH/math.cos(sLat)
    sHN = 1
    for k in range(0,20):
        RDistance = k*DataDistance
        DataX = RDistance * sinA
        DataX = abs(DataX) - Resolution / 2.0
        if DataX <= 0.0:
            NyStation = i
        else:
            Nxdirect = int(DataX / Resolution) + 1
            if sinA <= 0.0:
                NyStation = i + Nxdirect
            else:
                NyStation = i - Nxdirect
        DataY = RDistance * cosA
        DataY = abs(DataY) - Resolution / 2.0
        if DataY <= 0.0:
            NxStation = j
        else:
            Nydirect = int(DataY / Resolution) + 1
            if cosA <= 0.0:
                NxStation = j - Nydirect
            else:
                NxStation = j + Nydirect
        NxStation = max(1, min(NxStation, sNumRow))
        NyStation = max(1, min(NyStation, sNumColumn))
        TanSlope = (Alt[NxStation, NyStation] - Alt[i, j])/RDistance
        if TanSlope > TanH:
            sHN = 0
    print sHN
    return sHN


def CVA(N, D, X, JULDAY, sLat, Slope, sAspect):
    Aspect = sAspect * PI180
    TD = 15.0 * PI180
    W0 = 12.0 + X/TD
    if Aspect < PI/2:
        # Northeast
        ISP = 1
    elif Aspect >= PI/2 and Aspect <= PI:
        ISP = 2
        #southeast
        Aspect = PI - Aspect
    elif Aspect > PI and Aspect <= 1.5*PI:
        ISP = 3
        #southwest
        Aspect = Aspect - PI
    else:
        ISP = 4
        # Northwest
        Aspect = 2 * PI - Aspect
    iSun = [0 for i in range(N)]
    for i in range(0,N):
        XU = W0 + (i - 1) * D
        W = 15 * (XU - 12) * PI180
        sinH = math.sin(sLat) * math.sin(Declination) + math.cos(sLat) * math.cos(Declination) * math.cos(W)
        H = max(0.0,math.asin(sinH))
        cosH = math.cos(math.asin(sinH))
        cosB = (sinH*math.sin(sLat)-math.sin(Declination))/cosH/math.cos(sLat)
        cosB = max(-1.0,min(1.0,cosB))
        Alpha = math.acos(cosB)
        S1 = 0.0
        if ISP == 1:
            if XU < 12.0:
                if Alpha >= PI/2 - Aspect:
                    Beta = 0.0
                else:
                    S1 = PI/2-Alpha-Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            else:
                if Alpha >= PI/2+Aspect:
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
                if Alpha <= PI/2+Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI/2 - Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            # afternoon
            else:
                if Alpha <= PI/2-Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI/2 + Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
        elif ISP == 3:
            # morning
            if XU < 12.0:
                if Alpha <= PI/2-Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI/2 + Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            # afternoon
            else:
                if Alpha <= PI/2+Aspect:
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
                if Alpha <= PI/2+Aspect:
                    Beta = 0.0
                else:
                    S1 = Alpha - PI/2 + Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
            # afternoon
            else:
                if Alpha <= PI/2-Aspect:
                    Beta = 0.0
                else:
                    S1 = PI / 2 - Alpha - Aspect
                    tanB = math.tan(Slope) * math.sin(S1)
                    Beta = math.atan(tanB)
                if H >= Beta:
                    iSun[i] = 1
                else:
                    iSun[i] = 0
    return iSun


def TimeAngleBE(x,Nx):
    m = 1
    xx = [0 for i in range(Nx)]
    w1 = [0 for i in range(Nx)]
    w2 = [0 for i in range(Nx)]
    Warray = []
    for j in range(0, Nx):
        if x[j] > 0.25:
            xx[j] = j
            m = m + 1
    iNumberXX = m -1
    if iNumberXX == 0.0:
        LNumber = 1
        w1[0] = 1.0
        w2[0] = 1.0
    n = 2
    w1[0] = xx[0]
    for k in range(1,iNumberXX+1):
        if xx[k] != xx[k-1] + 1.0:
            w1[n] = xx[k]
            w2[n-1] = xx[k-1]
            n = n + 1
    w2[n-1] = xx[iNumberXX]
    LNumber = n-1
    return (w1,w2,LNumber)

def AccumDay(E0, Declination, u, v, w, w1, w2, LNumber):
    Accumarray = []
    DayRad = 0.0
    DayLength = 0.0
    for i in range(1,LNumber+1):
        DayLength = DayLength + (w2[i] - w1[i])
        DayRad = DayRad+0.082*E0*1440.0*(u*math.sin(Declination)*(w2[i]-w1[i])+v*math.cos(Declination)*(math.sin(w2[i])-math.sin(w1[i]))-w * math.cos(Declination)*(math.cos(w2[i])-math.cos(w1[i])))/(2.0*PI)
    DayLength = DayLength/0.261799
    return (DayRad,DayLength)
    
def getMouRad():
    for i in range(0, sNumColumn):
        sLat = gt[3] + gt[5] * i
        sLat = float(sLat)
        jd = int(ss)
        Declination,DayL,ARad,TAss,E0 = LevAstRad(sLat, jd)
        sDayLevHur = []
        sDayMouHur = []
        sDayLevRad = []
        sDayMouRad = []
        for j in range(0, sNumRow):
            if float(Aspect[i][j]) == 9999.0:
                #sDayLevHur = 9999.0
                #sDayMouHur = 9999.0
                #sDayLevRad = 9999.0
                #sDayMouRad = 9999.0
                sDayLevHur.append(9999.0)
                sDayMouHur.append(9999.0)
                sDayLevRad.append(9999.0)
                sDayMouRad.append(9999.0)
            else:
                sAspect = (float(Aspect[i][j]) - 180.0) * PI180
                sSlope = float(Slope[i][j]) * PI180
                u = math.sin(sLat) * math.cos(sSlope) - math.cos(sLat) * math.sin(sSlope) * math.cos(sAspect)
                v = math.cos(sLat) * math.cos(sSlope) + math.sin(sLat) * math.sin(sSlope) * math.cos(sAspect)
                w = math.sin(sAspect) * math.sin(sSlope)
                sDayLevHur.append(DayL)
                sDayLevRad.append(ARad)
                NDataTime = int(DayL * TD / DataTime) + 1
                NTime = NDataTime + 1
                TASS = TAss
                TimeAngle = [0 for i in range(NTime)]
                for k in range(0, NTime-1):
                    TimeAngle[k] = -TASS + DataTime * (k - 1)
                TimeAngle[NTime-1] = TASS
                sWtimeHN = [0 for i in range(NTime)]
                for k in range(0, NTime):
                    TAngle = TimeAngle[k]
                    sHN = HaveORNot(i, j, sLat, Altitude, sNumRow, sNumColumn, Declination, TAngle)
                    sWtimeHN[k] = sHN
                iSun = CVA(NTime, DataTime, TimeAngle[0], jd, sLat, sSlope, Aspect[i][j])
                for k in range(0, NTime):
                    sWtimeHN[k] = min(sWtimeHN[k], iSun[k])
                w1,w2,LNumber = TimeAngleBE(sWtimeHN, NTime)
                for k in range(1, LNumber + 1):
                    m = int(w1[k])
                    n = int(w2[k])
                    w1[k] = TimeAngle[m]
                    w2[k] = TimeAngle[m]
                print Declination
                DayRad,DayLength = AccumDay(E0, Declination, u, v, w, w1, w2, LNumber)
                sDayMouHur.append(DayLength)
                sDayMouRad.append(DayRad)
                print sDayLevHur,sDayLevRad,sDayMouHur,sDayMouRad
        #F = open(r"C:\Users\George\Desktop\pythontest\output.txt","w")
        #F.writelines(sDayLevHur+","+sDayLevRad+","+sDayMouHur+","+sDayMouRad)
        sDayLevHur = []
        sDayMouHur = []
        sDayLevRad = []
        sDayMouRad = []
    return 0
    
#if __name__ =='__main__':
getMouRad()


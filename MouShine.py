# -*- coding: cp936 -*-


import os
import datetime
import math
# from DayTotalRadiance import LevAstRad
# from test import GetCoeffab
#from test import GetCoeffAB
# from test import GetLL
from LevCalRad import LevAstRad
from InOrNot import HaveORNot
from CalCvDegree import CVA
from Tbeforend import TimeAngleBE
from CoverDegreeCal import CoverDegree
import numpy as np
import arcpy
from osgeo import gdal

from osgeo import osr
from osgeo import gdal_array


SunPara = 1366.7
PI = math.pi
PI180 = math.pi / 180.0
SunPara = 1366.7
NDirect = 14
NDirectAngle = 8
DataDistance = 1000.0
DataTime = 5.0
DataTime = DataTime*(PI/720)
TD = 15.0 * PI180
Resolution = 1000.0
CVDatadistance = 1000.0
#Found = "99.0"
#outputresult = "C:\Users\George\Desktop\pythontest\output.txt"

#idw = "C:/Users/George/Desktop/pythontest/testgeo/20121.tif"
#s1 = idw.index("2012")
#s2 = idw.index(".tif")
#ss = idw[s1 + 4:s2]

os.chdir("D://testimage//htgytest")

#in_xy = arcpy.Raster("altitude.tif")
#in_slope = arcpy.Raster("slope.tif")
#in_aspect = arcpy.Raster("aspect.tif")
#in_totalrad = arcpy.Raster("totalrad.tif")
#in_dirrad = arcpy.Raster("dirrad.tif")
#in_difrad = arcpy.Raster("difrad.tif")
#in_RefRad = arcpy.Raster("albedo20121.tif")
raster = gdal.Open("aspect.tif")
gt = raster.GetGeoTransform()
print raster.GetProjectionRef()
#extent = in_xy.extent
sNumColumn = raster.RasterXSize
sNumRow = raster.RasterYSize
XDirection = gt[1]
YDirection = gt[2]

#print extent,sNumColumn,XDirection
#print in_xy.width,in_xy.height
#print extent.XMin,extent.YMin,extent.XMax,extent.YMax
#Slope = arcpy.RasterToNumPyArray(in_slope,nodata_to_value=9999.0)
#Slope = arcpy.RasterToNumPyArray(in_slope)
#Aspect = arcpy.RasterToNumPyArray(in_aspect,nodata_to_value=9999.0)
#Aspect = arcpy.RasterToNumPyArray(in_aspect)
#Altitude = arcpy.RasterToNumPyArray(in_xy,nodata_to_value=9999.0)

#LevTotRad = arcpy.RasterToNumPyArray(in_totalrad,nodata_to_value=9999.0)
#LevDirRad = arcpy.RasterToNumPyArray(in_dirrad,nodata_to_value=9999.0)
#LevDifRad = arcpy.RasterToNumPyArray(in_difrad,nodata_to_value=9999.0)
#RefRadCoeff = arcpy.RasterToNumPyArray(in_RefRad,nodata_to_value=9999.0)
#Slope = arcpy.RasterToNumPyArray(in_slope,nodata_to_value=9999.0)
Slope = gdal_array.LoadFile("slope.tif")
Aspect = gdal_array.LoadFile("aspect.tif")
Altitude = gdal_array.LoadFile("altitude.tif")
LevTotRad = gdal_array.LoadFile("totalrad.tif")
LevDirRad= gdal_array.LoadFile("dirrad.tif")
LevDifRad= gdal_array.LoadFile("difrad.tif")
RefRadCoeff= gdal_array.LoadFile("albedo20121.tif")

#driver = gdal.GetDriverByName('GTiff')

output_raster = gdal.GetDriverByName('GTiff').Create('myraster.tif', sNumColumn, sNumRow, 1,gdal.GDT_Float32)  # Open the file
output_raster.SetGeoTransform(gt)  # Specify its coordinates
srs = osr.SpatialReference()  # Establish its coordinate encoding
srs.ImportFromWkt(raster.GetProjectionRef()) # This one specifies WGS84 lat long.
# Anyone know how to specify the
# IAU2000:49900 Mars encoding?
output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system

def GetGeoInfo(FileName):
    SourceDS = gdal.Open(FileName, gdal.GA_ReadOnly)
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())
    return GeoT, Projection

def CreateGeoTiff(Name, Array, driver,xsize, ysize, GeoT, Projection):
    DataType = gdal.GDT_Float32
    NewFileName = Name+'.tif'
    # Set up the dataset
    DataSet = driver.Create(NewFileName, xsize, ysize, 1, DataType)
    # the '1' is for band 1
    DataSet.SetGeoTransform(GeoT)
    DataSet.SetProjection(Projection.ExportToWkt())
    # Write the array
    DataSet.GetRasterBand(1).WriteArray(Array)
    return NewFileName



#print Altitude[0][0]
#Altitude = arcpy.RasterToNumPyArray(in_xy)
#xy_band = in_xy.GetRasterBand(1)
#Slope = slope_band.ReadAsArray()
#gt = in_xy.GetGeoTransform()
#print xy_band.YSize
#print gt[0], gt[3], gt[0] + gt[1] * idw_band.XSize, gt[3] + gt[5] * idw_band.YSize
#print gt[0], gt[3], gt[0] + gt[1] * xy_band.XSize, gt[3] + gt[5] * xy_band.YSize



def AccumDay(E0, Declination, u, v, w, w1, w2, LNumber):
    #Accumarray = []
    DayRad = 0.0
    DayLength = 0.0
    for i in range(0, LNumber):
        DayLength = DayLength + (w2[i] - w1[i])
        #print DayLength
        DayRad = DayRad + 0.082 * E0 * 1440.0 * (u * math.sin(Declination)*(w2[i] - w1[i]) + v * math.cos(Declination)*(math.sin(w2[i]) - math.sin(w1[i])) - w * math.cos(Declination) * (math.cos(w2[i]) - math.cos(w1[i]))) / (2.0 * PI)
    DayLength = DayLength/0.261799
    return (DayRad, DayLength)

def getMouRad():
    #F = open(r"C:\Users\George\Desktop\pythontest\TotalRad.txt", "w")
    #F = open(r"C:\Users\George\Desktop\pythontest\DayRad.txt", "w")
    #print sNumRow,sNumColumn
    outputarray = []
    for i in range(0, sNumRow):
        #print extent.YMin
        #ActDirRad = 0.0
        #ActDifRad = 0.0
        #ActDifRad = 0.0
        #print extent.YMax
        sLat = gt[3] + gt[5] * i
        #print sLat
        sLat = float(sLat)
        sLat = PI * sLat / 180
        jd = 1
        DayL, ARad, TAss, E0, Declination = LevAstRad(sLat, jd)
        sDayLevHur = []
        sDayMouHur = []
        sDayLevRad = []
        sDayMouRad = []
        ActTotRadarray = []
        DayRadarray = []
        irow = i
        print irow
        #print DayL, ARad, TAss, E0, Declination
        for j in range(0, sNumColumn):
            #print j
            #print extent.XMin + XDirection*j
            aspectorno = float(Aspect[i][j])
            if aspectorno == 9999.0:
                #print i, j
                sDayLevHur.append(9999.0)
                sDayMouHur.append(9999.0)
                sDayLevRad.append(9999.0)
                sDayMouRad.append(9999.0)
                ActTotRadarray.append(9999.0)
                DayRadarray.append(9999.0)
            else:
                #print irow
                #print i,j
                sAspect = (float(Aspect[i][j])-180.0) * PI180
                sSlope = float(Slope[i][j]) * PI180
                u = math.sin(sLat) * math.cos(sSlope) - math.cos(sLat) * math.sin(sSlope) * math.cos(sAspect)
                v = math.cos(sLat) * math.cos(sSlope) + math.sin(sLat) * math.sin(sSlope) * math.cos(sAspect)
                w = math.sin(sAspect) * math.sin(sSlope)
                sDayLevHur.append(DayL)
                sDayLevRad.append(ARad)
                NDataTime = int(DayL*TD/DataTime) + 1
                NTime = NDataTime + 1
                TASS = TAss
                TimeAngle = [0 for ii in range(NTime)]
                for k in range(0, NTime-1):
                    TimeAngle[k] = -TASS + DataTime*k
                TimeAngle[NTime-1] = TASS
                sWtimeHN = [0 for iii in range(NTime)]
                jcolumn = j
                for k in range(0, NTime):
                    TAngle = TimeAngle[k]
                    sHN = HaveORNot(irow,jcolumn, sLat, Altitude, sNumRow, sNumColumn, Declination, TAngle)
                    sWtimeHN[k] = sHN
                #print sWtimeHN
                Aspectofcv = Aspect[i][j]
                iSun = CVA(NTime, DataTime, TimeAngle[0], jd, sLat, sSlope, Aspectofcv, Declination)
                #print iSun
                for k in range(0, NTime):
                    sWtimeHN[k] = min(sWtimeHN[k], iSun[k])
                #print sWtimeHN,iSun
                w1, w2, LNumber = TimeAngleBE(sWtimeHN, NTime)
                #print w1
                #print w2
                #print LNumber
                for k in range(0, LNumber):
                    m = int(w1[k])-1
                    n = int(w2[k])-1
                    w1[k] = TimeAngle[m]
                    w2[k] = TimeAngle[n]
                DayRad, DayLength = AccumDay(E0, Declination, u, v, w, w1, w2, LNumber)
                #print DayRad,DayLength
                DayRadarray.append(DayRad)
                CV = CoverDegree(i, j, Altitude, sNumRow, sNumColumn)
                #CV = (1+math.cos(Aspectofcv*PI180))/2
                #print CV
                LRR = float(LevDirRad[i][j])
                LFR = float(LevDifRad[i][j])
                LTR = float(LevTotRad[i][j])
                RRC = float(RefRadCoeff[i][j])
                if RRC == 9999.0:
                    RRC = 0.15
                ActDirRad = LRR * (DayRad/ARad)
                sKb = LRR/ARad
                sRb = DayRad/ARad
                ActDifRad = LFR * (sKb * sRb + CV * (1.0 - sKb))
                ActRefRad = LTR *RRC* (1.0 - CV)
                ActTotRad = ActDirRad + ActDifRad + ActRefRad
                #ActTotRadarray.append(ActTotRad)
                if ActTotRad >=0 and ActTotRad<=30:
                    ActTotRadarray.append(ActTotRad)
                else:
                    ActTotRadarray.append(9999.0)
        outputarray.append(ActTotRadarray)
    array = np.asarray(outputarray).astype(np.float32)
    # Writes my array to the raster
    output_raster.GetRasterBand(1).WriteArray(array)
    #without setting the nodatavalue, the tiff will not visiualize normally
    output_raster.GetRasterBand(1).SetNoDataValue(9999)
    output_raster.FlushCache()
    #NewFileName = CreateGeoTiff('ouput',array, driver, XDirection, YDirection, GeoT, Projection)
    #myRaster = arcpy.NumPyArrayToRaster(np.asarray(outputarray), x_cell_size=XDirection)
    #myRaster.save("D:/testimage/xxraster.gdb/Raster1")
    #F.writelines(str(ActTotRadarray)+"\n")
    return 0
if __name__ =='__main__':
    #print 1
    getMouRad()
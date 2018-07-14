# -*- coding: cp936 -*-
import os
import datetime
import math
from DayTotalRadiance import LevAstRad
from test import GetCoeffab
from test import GetCoeffAB
from test import GetLL
import numpy as np
import arcpy
from arcpy import env

outpath = 'C:\Users\George\Desktop\pythontest\htgy2012'
env.overwriteOutput=True
env.workspace= outpath

PI = math.pi
#StaSunArray = []
#testarray = []

# def getsunshinetime(folderpath):
#     sunarray = []
#     sourcepath = folderpath
#     #year = [2008,2009,2010,2011,2012,2013]
#     year = 2008
#     namearray = []
#     LDayTotRad = []
#     LDayDirRad = []
#     LDayDifRad = []
#     for i in range(0,14):
#         staID = LCoeffab[i][1][0]
#         sLat  = LCoeffab[i][1][1]
#         #sLong = LCoeffab[i][1][2]
#         #sHeight = LCoeffab[i][1][3]
#         sLat = float(sLat)
#         #sLong = float(sLong)
#         #print sLat
#         coeffab = LCoeffab[i]
#         path = sourcepath+'\\'+staID+'\\'+'日照时数'
#         print path
#         #print path
#         nameID = staID
#         #for ii in range(len(year)):
#         name = nameID+str(year)
#         #print name
#         namearray.append(name)
#         #指定txt路径
#         sDayTotRad = []
#         sDayDirRad = []
#         sDayDifRad = []
#         for r,ds,fs in os.walk(path):
#             for f in fs:
#                 #如果在[2008-2013],则读取文件
#                 if f[:-4] in namearray:
#                     filename = r+"\\"+f
#                     txthandle = open(filename,'rb')
#                     cline = txthandle.readlines()
#                     for i in range(0,len(cline)):
#                         sline = cline[i].split(" ")
#                         array = filter(None,sline)
#                         year = array[0]
#                         month = array[1]
#                         day = array[2]
#                         #shapefilename = year+month+day+".shp"
#                         shinetime = array[3]
#                         shinetime = float(shinetime)
#                         #jd = JD0(year,month,day)
#                         #print array[0],array[1],array[2],array[3]
#                         #计算年积日-----------
#                         fmt = '%Y.%m.%d'
#                         s = year+'.'+month+'.'+day
#                         jd = datetime.datetime.strptime(s, fmt).timetuple().tm_yday
#                         #print jd
#                         result = LevAstRad(sLat,jd)
#                         DayL = result[1]
#                         DayL = float(DayL)
#                         R = shinetime/DayL
#                         ARad = result[2]
#                         m = int(month)-1
#                         DayTotRad = float(ARad)*(float(coeffab[m][2])+float(R)*float(coeffab[m][3]))
#                         DayDirRad = float(ARad)*(R*float(arrayAB[m][0])+ math.pow(R,2)*float(arrayAB[m][1]))
#                         DayDifRad = DayTotRad - DayDirRad
#                         sDayTotRad.append(DayTotRad)
#                         #print len(sDayTotRad)
#                         sDayDirRad.append(DayDirRad)
#                         #print len(sDayDirRad)
#                         sDayDifRad.append(DayDifRad)
#                         #print len(sDayDifRad)
#                         #jd_shinetime = [jd,shinetime]
#                         #sunarray.append(jd)
#                         #sunarray.append(shinetime)
#                         #年积日计算结束------------
#         #sDayTotRad = np.asarray(sDayTotRad)
#         #sDayTotRad.T
#         #print len(sDayTotRad)
#         LDayTotRad.append(sDayTotRad)
#         #sDayDirRad = np.asarray(sDayDirRad)
#         #sDayDirRad.T
#         LDayDirRad.append(sDayDirRad)
#         #sDayDifRad = np.asarray(sDayDifRad)
#         #sDayDifRad.T
#         LDayDifRad.append(sDayDifRad)
#     for ii in range(0,366):
#         shapefilename = "2008"+str(ii)+".shp"
#         arcpy.CreateFeatureclass_management(outpath, shapefilename, "POINT")
#         arcpy.AddField_management(shapefilename, "staID", "string", field_length=20)
#         arcpy.AddField_management(shapefilename, "sHeight", "string", field_length=20)
#         arcpy.AddField_management(shapefilename, "DayTotRad", "float", field_length=20)
#         arcpy.AddField_management(shapefilename, "DayDirRad", "float", field_length=20)
#         arcpy.AddField_management(shapefilename, "DayDifRad", "float", field_length=20)
#         fields = ['staID', 'sHeight', 'DayTotRad', 'DayDirRad', 'DayDifRad']
#         for jj in range(0,14):
#             staID = LLarray[jj][0]
#             sY = LLarray[jj][1]
#             sX = LLarray[jj][2]
#             sHeight = LLarray[jj][3]
#             #print staID,sLat,sLong,sHeight
#             rowInserter = arcpy.InsertCursor(shapefilename, fields)
#             pointGeometry = arcpy.Point(sY, sX)
#             newPoint = rowInserter.newRow()
#             newPoint.shape = pointGeometry
#             print pointGeometry.X,pointGeometry.Y
#             newPoint.staID = staID
#             newPoint.sHeight = sHeight
#             newPoint.DayTotRad = LDayTotRad[jj][ii]
#             newPoint.DayDirRad = LDayDirRad[jj][ii]
#             newPoint.DayDifRad = LDayDifRad[jj][ii]
#             rowInserter.insertRow(newPoint)
#             print "pick up Successfully...."
#             #print str(ii)+"----"+str(jj)
#             del rowInserter
#     return 0


def getsolartime(folderpath):
    sunarray = []
    sourcepath = folderpath
    #year = [2008,2009,2010,2011,2012,2013]
    year = 2012
    namearray = []
    LDayTotRad = []
    LDayDirRad = []
    LDayDifRad = []
    for i in range(0,13):
        staID = LCoeffab[i][1][0]
        sLat  = LCoeffab[i][1][1]
        #sLong = LCoeffab[i][1][2]
        #sHeight = LCoeffab[i][1][3]
        sLat = float(sLat)
        #sLong = float(sLong)
        #print sLat
        coeffab = LCoeffab[i]
        path = sourcepath+'\\'+staID+'.txt'
        print path
        #print path
        nameID = staID
        #for ii in range(len(year)):
        name = nameID+str(year)
        #print name
        namearray.append(name)
        #指定txt路径
        sDayTotRad = []
        sDayDirRad = []
        sDayDifRad = []

        txthandle = open(path,'rb')
        cline = txthandle.readlines()
        startdateline = cline[0].split("    ")
        startyear = int(startdateline[1])
        startmonth = int(startdateline[2])
        startday = int(startdateline[3])

        d1 = datetime.datetime(startyear, startmonth, startday)
        d2 = datetime.datetime(2012,1,1)
        days = (d2 - d1).days
        print days
        for i in range(days, days+366):
            sline = cline[i].split("    ")
            print sline
            array = filter(None, sline)
            year = array[1]
            month = array[2]
            day = array[3]
            # shapefilename = year+month+day+".shp"
            shinetime = array[4]
            shinetime = float(shinetime)
            # jd = JD0(year,month,day)
            # print array[0],array[1],array[2],array[3]
            # 计算年积日-----------
            fmt = '%Y.%m.%d'
            s = year + '.' + month + '.' + day
            jd = datetime.datetime.strptime(s, fmt).timetuple().tm_yday
            # print jd
            result = LevAstRad(sLat, jd)
            DayL = result[1]
            DayL = float(DayL)            R = shinetime / DayL
            ARad = result[2]
            m = int(month) - 1
            DayTotRad = float(ARad) * (float(coeffab[m][2]) + float(R) * float(coeffab[m][3]))
            DayDirRad = float(ARad) * (R * float(arrayAB[m][0]) + math.pow(R, 2) * float(arrayAB[m][1]))
            DayDifRad = DayTotRad - DayDirRad
            sDayTotRad.append(DayTotRad)
            # print len(sDayTotRad)
            sDayDirRad.append(DayDirRad)
            # print len(sDayDirRad)
            sDayDifRad.append(DayDifRad)


        LDayTotRad.append(sDayTotRad)
        #sDayDirRad = np.asarray(sDayDirRad)
        #sDayDirRad.T
        LDayDirRad.append(sDayDirRad)
        #sDayDifRad = np.asarray(sDayDifRad)
        #sDayDifRad.T
        LDayDifRad.append(sDayDifRad)
    for ii in range(0,366):
        shapefilename = "2012"+str(ii)+".shp"
        arcpy.CreateFeatureclass_management(outpath, shapefilename, "POINT")
        arcpy.AddField_management(shapefilename, "staID", "string", field_length=20)
        arcpy.AddField_management(shapefilename, "sHeight", "string", field_length=20)
        arcpy.AddField_management(shapefilename, "DayTotRad", "float", field_length=20)
        arcpy.AddField_management(shapefilename, "DayDirRad", "float", field_length=20)
        arcpy.AddField_management(shapefilename, "DayDifRad", "float", field_length=20)
        fields = ['staID', 'sHeight', 'DayTotRad', 'DayDirRad', 'DayDifRad']
        for jj in range(0,13):
            staID = LLarray[jj][0]
            sY = LLarray[jj][1]
            sX = LLarray[jj][2]
            sHeight = LLarray[jj][3]
            #print staID,sLat,sLong,sHeight
            rowInserter = arcpy.InsertCursor(shapefilename, fields)
            pointGeometry = arcpy.Point(sY, sX)
            newPoint = rowInserter.newRow()
            newPoint.shape = pointGeometry
            #print pointGeometry.X,pointGeometry.Y
            newPoint.staID = staID
            newPoint.sHeight = sHeight
            newPoint.DayTotRad = LDayTotRad[jj][ii]
            newPoint.DayDirRad = LDayDirRad[jj][ii]
            newPoint.DayDifRad = LDayDifRad[jj][ii]
            rowInserter.insertRow(newPoint)
            print "pick up Successfully...."
            #print str(ii)+"----"+str(jj)
            del rowInserter
    return 0




if __name__ =='__main__':
    txtpath1 = 'C:\Users\George\Desktop\pythontest\\abCoeff.txt'
    txtpath2 = 'C:\Users\George\Desktop\pythontest\\abCoeff_LP.txt'
    txtpath3 = "C:\Users\George\Desktop\pythontest\Prj_coords.txt"
    folderpath = r'C:\Users\George\Desktop\solar radiation'
    arrayAB = GetCoeffAB(txtpath1)
    #print arrayAB
    LCoeffab = GetCoeffab(txtpath2)
    print LCoeffab[12][1]
    LLarray = GetLL(txtpath3)
    print LLarray[12]
    getsolartime(folderpath)
    #staID = GetCoeffab(txtpath2)

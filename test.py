# -*- coding: cp936 -*-

import os
import datetime
import math
PI = math.pi
#arrayAB = []

def GetCoeffAB(txtpath):
    txthandle = open(txtpath,'rb')
    cline = txthandle.readlines()
    arrayAB = []
    for i in range(0,len(cline)-1):
        sline = cline[i].split("	")
        array = filter(None,sline)
        print array
        CoeffA = array[0]
        CoeffB = array[1]
        CoeffAB = [CoeffA,CoeffB]
        arrayAB.append(CoeffAB)
        #print array[0],array[1]
    return arrayAB

def GetLL(txtpath):
    txthandle = open(txtpath,'rb')
    cline = txthandle.readlines()
    LL = []
    for i in range(0,len(cline)):
        sline = cline[i].split(",")
        array = filter(None,sline)
        sID = array[0]
        Lat = array[1]
        Long = array[2]
        Hight = array[3]
        singleLL = [sID,Lat,Long,Hight]
        LL.append(singleLL)
        #LL.append(Lat)
        #LL.append(Long)
        #LL.append(Hight)
        #print array[0],array[1]
    return LL

        
def GetCoeffab(txtpath):
    txthandle = open(txtpath,'rb')
    cline = txthandle.readlines()
    coeffarray = []
    coeffbrray = []
    Lcoeffarray = []
    Lcoeffbrray = []
    staID = []
    for i in range(0,len(cline)):
        sline = cline[i].split("	")
        array = filter(None,sline)
        #print array
        ID = array[0]
        Lat = array[1]
        Long = array[2]
        staID.append(ID)
        #print array[0],array[1],array[2],array[3]
        for  k in range(1,13):
            coeffa = array[4+(k-1)*2]
            coeffb = array[3+ k*2]
            coeffab = [ID,Lat,coeffa,coeffb]
            coeffarray.append(coeffab)
            #print len(coeffarray)
            #coeffbrray.append(coeffb)
            #print len(coeffbrray)
        Lcoeffarray.append(coeffarray)
        #Lcoeffbrray.append(coeffbrray)
        coeffarray = []
        #coeffbrray = []
    #print Lcoeffarray[0][0],Lcoeffbrray[0][0]
    return Lcoeffarray


##if __name__ =='__main__':
##    txtpath1 = 'C:\Users\George\Desktop\pythontest\CoeffAB.txt'
##    txtpath2 = 'C:\Users\George\Desktop\pythontest\Coeff_ab.txt'
##    folderpath = r'C:\Users\George\Desktop\pythontest\xianyang'
##    #GetCoeffAB(txtpath1)
##    res = GetCoeffab(txtpath2)
##    #res为14*12数组
##    print len(res)
##    print res[0]
##    print res[1]
##    #staID = GetCoeffab(txtpath2)
##    #getsunshinetime(folderpath,staID)

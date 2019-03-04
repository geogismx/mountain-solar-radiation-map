# -*- coding: cp936 -*-

import os
import datetime
import math
PI = math.pi
SunPara = 1366.7
#from test import getGetCoeffab
#from test import getsunshinetime


def LevAstRad(sLat,jd):
    result = []
    JulDAY = jd
    DayA = 2*PI*(JulDAY-1)/365.2422
    sLat = PI*sLat/180
    Dec = 0.4102*math.sin(2*PI*(JulDAY-80)/365.0)
    #Dec = 0.006894-0.399512*math.cos(DayA)+0.072075*math.sin(DayA)-0.006799*math.cos(2*DayA)+0.000896*math.sin(2*DayA)-0.002689*math.cos(3*DayA)+0.001516*math.sin(3*DayA)
    coshaf = 0.0 - math.tan(sLat)*math.tan(Dec)
    if coshaf >= 1.0:
        TAss = PI
    else:
        TAss = math.acos(coshaf)   
    DayL = 2.0*TAss/0.261799
    E0 = 1.000109+0.033494*math.cos(DayA)+0.001472*math.sin(DayA)+0.000768*math.cos(2.0*DayA)+0.000079*math.sin(2.0*DayA)
    ARad = SunPara*E0*(24.0*3600.0)/PI*(TAss*math.sin(sLat)*math.sin(Dec)+math.cos(sLat)*math.cos(Dec)*math.sin(TAss))
    ARad = ARad/1000000.0
    result.append(Dec)
    result.append(DayL)
    result.append(ARad)
    return result



 



# -*- coding: cp936 -*-

import os
import datetime
import math
import numpy as np


path = r'D:\data\climate sites data\sites of climate for radiation\sourcedata\日照时数'

for d in os.listdir(path):
    txt = os.path.join(path,d)
    outpath = 'D:\data\climate sites data\sites of climate for radiation\\'+ d
    Txtfile = open(outpath, 'w')
    txthandle = open(txt, 'rb')
    clines = txthandle.readlines()
    for i in range(0, len(clines)):
        sline = clines[i].split(" ")
        array = filter(None, sline)
        name = array[0]
        year = array[1]
        month = array[2]
        day = array[3]
        solartime = array[10]
        cline = name+"    "+year+"    "+month+"    "+day+"    "+solartime
        Txtfile.writelines(cline+'\n')


# -*- coding: cp936 -*-

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import csv
#os.chdir(r'C://Users//George//Desktop//Paper_results//52866')

### deal with the file like RADI_MUL_CHN_DAY-201703, and output it with header for R
os.chdir(r'D://data//climate sites data//太阳辐射数据//SUN_DAY')

flist = os.listdir(r'D://data//climate sites data//太阳辐射数据//SUN_DAY')
print len(flist)


for i in range(0,len(flist)):
    f = open(flist[i])
    ### get filename
    filename = flist[i][-10:-4]
    print filename
    ### specify the output filename of csv
    resultFile = open('Sun' + filename + '.txt', 'w')
    ## add header to file
    header = 'ID' + ',' + 'Y' + ',' + 'M' + ',' + 'D' + ',' + 'Sun'
    resultFile.write(header + '\n')

    for line in f:
        line = line.rstrip()
        vals = line.split(" ")
        ### filter none string in list
        str_list = filter(None, vals)
        ### delete the missing value
        if str_list[7] == '32766':
            str_list[7] = '0'
            row = str_list[0]+','+str_list[4]+','+str_list[5]+','+str_list[6]+','+str_list[7]
            resultFile.write(row+'\n')
        else:
            row = str_list[0]+','+str_list[4]+','+str_list[5]+','+str_list[6]+','+str_list[7]
            resultFile.write(row+'\n')
    f.close()

    #df2 = pd.read_csv('52866'+str(i)+'.txt',header=None)
    #columns = ['Y', 'M', 'D', 'Rad']
    #df2.reindex(columns=columns)
    #print df2
    #df2[columns] = df2[columns].astype(int)
    #result = pd.concat([df1, df2], axis=1)
    #print result[['ID']]




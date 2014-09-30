# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
import random

print 'Ready'
line = []
f = codecs.open('station_Aotizhongxin.txt', 'r',"utf-8")
line = f.readlines()
f.close()

random.shuffle(line)

for i in range(4):
    f_train = codecs.open('station_Aotizhongxin_train%d.txt'%(i+1), 'w',"utf-8")
    f_test = codecs.open('station_Aotizhongxin_test%d.txt'%(i+1), 'w',"utf-8")
    for t in range(len(line)):
        if(t>=i*1000 and t<(i+1)*1000):
            f_test.write(line[t])
        else:
            f_train.write(line[t])
    f_train.close()
    f_test.close()

    

    
print 'End'

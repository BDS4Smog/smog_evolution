# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
import time
import random

STATION = 'haidian'
TYPE = 'low'

def get_time_list():
    ifile=codecs.open(u''+STATION+'_'+TYPE+'_all.txt', 'r',"utf-8") 
    tmp_list = ifile.readlines()
    random.shuffle(tmp_list)
    tmp_list = tmp_list[0:99]
    return tmp_list

def write_time_list(time_list):
    ofile=codecs.open(u''+STATION+'_'+TYPE+'.txt', 'w',"utf-8") 
    for t in time_list:
    	ofile.write(t)

if __name__ == '__main__':
    print "Ready"
    time_list = get_time_list()
    write_time_list(time_list)

# -*- coding: utf-8 -*-
import pymongo
import os

import sys
import string
import codecs
import time
import random

ISOTIMEFORMAT='%Y-%m-%dT%XZ'
STEP = 6 
DIFF = 2

STATION = 'haidian'
STATION_C = '海淀区万柳'

TYPE = 'low'


stations = [u"药材公司",u"机车车辆厂",u"游泳馆",u"人民公园",u"化工学校"]  
cities = [u"廊坊",u"天津",u"保定",u"张家口",u"石家庄"]


conn = pymongo.Connection("10.214.0.147",27017)
db = conn.Air
db_weather = conn.forecastio
collection = db.Stations

ifile=codecs.open(u'events/'+STATION+'_'+TYPE+'.txt', 'r',"utf-8")
time_list = ifile.readlines()

ofile=codecs.open(u'data_spacial/'+STATION+'_'+TYPE+'_'+str(DIFF)+'h.txt', 'w',"utf-8")

record = [{}]*len(stations)
for i in range(len(stations)):
    record[i]={}
    print i
    print stations[i]
    print cities[i]
    tmp_record = collection.find({"position_name":stations[i],"area":cities[i]},{"time_point":1,"pm2_5":1})
    for r in tmp_record:
        record[i][r['time_point']] = r['pm2_5']
        if r['time_point']=='2014-04-28T22:00:00Z':
            print r['pm2_5']

record_main = {}
tmp_record = collection.find({"position_name":STATION_C,"area":u"北京"})
for r in tmp_record:
    record_main[r['time_point']] = r['pm2_5']


result = {}
m_result = [{}]*len(cities)


print 'Ready' 
for current_time in time_list:
    

    current_time = current_time.strip('\r\n')[0:19] + 'Z'
    unix_current = time.mktime(time.strptime(current_time,ISOTIMEFORMAT))
    
    for time_iter in range(0,STEP):
        unix_tmp = unix_current-time_iter*3600
        tmp_time = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
        tmp_time1 = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp-3600*DIFF))
        print tmp_time
        
        result["pm2_5"]=-1
        if record_main.has_key(tmp_time) and record_main[current_time]!=0:
            result["pm2_5"]=record_main[current_time]

        
        for city_iter in range(len(cities)):
            m_result[city_iter]={}
            m_result[city_iter]["3h"]=0
            
            if record[city_iter].has_key(tmp_time) and record[city_iter].has_key(tmp_time1):
                if record[city_iter][tmp_time]!=0 and record[city_iter][tmp_time1]!=0:
                    print city_iter
                    print record[city_iter][tmp_time]
                    print record[city_iter][tmp_time1]
                    m_result[city_iter]["3h"]=record[city_iter][tmp_time]-record[city_iter][tmp_time1]
                    

        ofile.write(tmp_time)
        ofile.write(" %d"%(result["pm2_5"]))
        for city_iter in range(len(cities)):
            ofile.write(" %d"%(m_result[city_iter]["3h"]))
        ofile.write("\r\n")

        
ofile.close()
ifile.close()

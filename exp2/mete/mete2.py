# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
import time
ISOTIMEFORMAT='%Y-%m-%dT%XZ'
STEP = 1 
STATION = 'haidian'
TYPE = 'low'

#import math
#connect

cities = ["北京"]
#stations = ["环境监测监理中心","万寿西宫","美国大使馆","官园","定陵","东四","天坛","顺义新城","昌平镇"]  
#cities = ["廊坊","北京","北京","北京","北京","北京","北京","北京","北京"]
#stations = ["海淀区万柳","市环保局","供销社","离宫","市环保局","黑马集团"]  
#cities = ["北京","沧州","唐山","承德","衡水","德州"]

init_time = "2014-01-01T00:00:00Z"
final_time = "2014-10-20T00:00:00Z"


def get_records():
    conn = pymongo.Connection("10.214.0.147",27017)
    db = conn.Air
    collection = db.Weather

    record = [{}]*len(cities)
    for i in range(len(cities)):
        record[i]={}
        print i
        print cities[i]
        tmp_record = collection.find({"area":cities[i]})
        for r in tmp_record:
            if r.has_key('time_point'):
                tmp = time.mktime(time.strptime(r['time_point'],ISOTIMEFORMAT))
                record[i][tmp]=r

    return record[0]

def get_time_list(station,mtype):
    ifile=codecs.open(u'../events/'+station+'_'+mtype+'.txt', 'r',"utf-8") 
    tmp_list = ifile.readlines()
    time_list = []
    for t in tmp_list:
        time_list.append(t.strip('\r\n')[0:19] + 'Z')
    return time_list

def pro_and_write_data(record,station,mtype):
    print record.keys()
    ofile=codecs.open(u'./'+station+'_'+mtype+'2.txt', 'w',"utf-8")
    result = {}
    for current_time in time_list:
        
        unix_current = time.mktime(time.strptime(current_time,ISOTIMEFORMAT))
        for time_iter in range(0,STEP):
            
            unix_tmp = unix_current-time_iter*3600
            tmp_time = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
            print tmp_time

            result["temperature"] = -1
            result["pressure"] = -1
            result["humidity"] = -1
            result["wind_speed_value"] = -1
            result["wind_direction_value"] = -1
            result["rain_3h"] = -1
            result["clouds_value"] = -1

            closest_record = record.get(unix_tmp, record[min(record.keys(), key=lambda k: abs(k-unix_tmp))])
           
            if closest_record.has_key('temperature'):
                result["temperature"] = closest_record['temperature']
            if closest_record.has_key('pressure'):
                result["pressure"] = closest_record['pressure']
            if closest_record.has_key('humidity'):
                result["humidity"] = closest_record['humidity']
            if closest_record.has_key('wind_speed_value'):
                result["wind_speed_value"] = closest_record['wind_speed_value']
            if closest_record.has_key('wind_direction_value'):
                result["wind_direction_value"] = closest_record['wind_direction_value']
            if closest_record.has_key('rain_3h') :
                result["rain_3h"] = closest_record['rain_3h']
            if closest_record.has_key('clouds_value') :
                result["clouds_value"] = closest_record['clouds_value']

            ofile.write(tmp_time)
            ofile.write(" %f %f %f %f %f %f %f"%(result["temperature"],result["pressure"],result["humidity"],result["wind_speed_value"],
                                                   result["wind_direction_value"],result["rain_3h"],result["clouds_value"]))
            ofile.write("\r\n")

            
    ofile.close()

if __name__ == '__main__':
    print "Ready"
    record = get_records()
    time_list = get_time_list('beijing','low')
    pro_and_write_data(record,'beijing','low')
    time_list = get_time_list('beijing','increase')
    pro_and_write_data(record,'beijing','increase')
    time_list = get_time_list('beijing','decrease')
    pro_and_write_data(record,'beijing','decrease')
    time_list = get_time_list('beijing','high')
    pro_and_write_data(record,'beijing','high')
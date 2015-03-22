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

stations = ["海淀区万柳"]  
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
    collection = db.Stations


    record = [{}]*len(stations)
    for i in range(len(stations)):
        record[i]={}
        print i
        print stations[i]
        print cities[i]
        tmp_record = collection.find({"position_name":stations[i],"area":cities[i]})
        for r in tmp_record:
            record[i][r['time_point']]={}
            record[i][r['time_point']]['pm2_5'] = r['pm2_5']
            record[i][r['time_point']]['pm10'] = r['pm10']
            record[i][r['time_point']]['no2'] = r['no2']
            record[i][r['time_point']]['so2'] = r['so2']
            record[i][r['time_point']]['co'] = r['co']
            record[i][r['time_point']]['o3'] = r['o3']

    return record[0]

def get_time_list(station,type):
    ifile=codecs.open(u'../events/'+station+'_'+type+'.txt', 'r',"utf-8") 
    tmp_list = ifile.readlines()
    time_list = []
    for t in tmp_list:
        time_list.append(t.strip('\r\n')[0:19] + 'Z')
    return time_list

def pro_and_write_data(record,station,type):
    ofile=codecs.open(u'./'+station+'_'+type+'1.txt', 'w',"utf-8")
    result = {}
    for current_time in time_list:
        
        unix_current = time.mktime(time.strptime(current_time,ISOTIMEFORMAT))
        for time_iter in range(0,STEP):
            
            unix_tmp = unix_current-time_iter*3600
            tmp_time = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
            print tmp_time

            result["pm2_5"]=-1
            result["pm10"]=-1
            result["no2"]=-1
            result["so2"]=-1
            result["co"]=-1
            result["o3"]=-1

            if record.has_key(tmp_time) and record[tmp_time]['pm2_5'] != 0:
                result["pm2_5"] = record[tmp_time]['pm2_5']
            if record.has_key(tmp_time) and record[tmp_time]['pm10'] != 0:
                result["pm10"] = record[tmp_time]['pm10']
            if record.has_key(tmp_time) and record[tmp_time]['no2'] != 0:
                result["no2"] = record[tmp_time]['no2']
            if record.has_key(tmp_time) and record[tmp_time]['so2'] != 0:
                result["so2"] = record[tmp_time]['so2']
            if record.has_key(tmp_time) and record[tmp_time]['co'] != 0:
                result["co"] = record[tmp_time]['co']
            if record.has_key(tmp_time) and record[tmp_time]['o3'] != 0:
                result["o3"] = record[tmp_time]['o3']

            ofile.write(tmp_time)
            ofile.write(" %d %d %d %d %f %d"%(result["pm2_5"],result["pm10"],result["no2"],result["so2"],result["co"],result["o3"]))

            ofile.write("\r\n")

            
    ofile.close()

if __name__ == '__main__':
    print "Ready"
    record = get_records()
    time_list = get_time_list('haidian','low')
    pro_and_write_data(record,'haidian','low')
    time_list = get_time_list('haidian','increase')
    pro_and_write_data(record,'haidian','increase')
    time_list = get_time_list('haidian','decrease')
    pro_and_write_data(record,'haidian','decrease')
    time_list = get_time_list('haidian','high')
    pro_and_write_data(record,'haidian','high')












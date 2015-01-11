# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
import time
ISOTIMEFORMAT='%Y-%m-%dT%XZ'
STEP = 1 
STATION = 'beijing'
TYPE = 'low'

#import math
#connect

cities = ["上海"]
#stations = ["环境监测监理中心","万寿西宫","美国大使馆","官园","定陵","东四","天坛","顺义新城","昌平镇"]  
#cities = ["廊坊","北京","北京","北京","北京","北京","北京","北京","北京"]
#stations = ["海淀区万柳","市环保局","供销社","离宫","市环保局","黑马集团"]  
#cities = ["北京","沧州","唐山","承德","衡水","德州"]

init_time = "2014-01-01T00:00:00Z"
final_time = "2014-10-20T00:00:00Z"


def get_records():
    conn = pymongo.Connection("10.214.0.147",27017)
    db = conn.Air
    collection = db.Cities


    record = [{}]*len(cities)
    for i in range(len(cities)):
        record[i]={}
        print i
        print cities[i]
        tmp_record = collection.find({"area":cities[i]})
        for r in tmp_record:
            if r.has_key('time_point'):
                record[i][r['time_point']]={}
                if r.has_key('aqi'):
                    record[i][r['time_point']]['aqi'] = r['aqi']
                else:
                    record[i][r['time_point']]['aqi'] = -1
                if r.has_key('pm2_5'):
                    record[i][r['time_point']]['pm2_5'] = r['pm2_5']
                else:
                    record[i][r['time_point']]['pm2_5'] = -1
                if r.has_key('pm10'):
                    record[i][r['time_point']]['pm10'] = r['pm10']
                else:
                    record[i][r['time_point']]['pm10'] = -1
                if r.has_key('no2'):
                    record[i][r['time_point']]['no2'] = r['no2']
                else:
                    record[i][r['time_point']]['no2'] = -1
                if r.has_key('so2'):
                    record[i][r['time_point']]['so2'] = r['so2']
                else:
                    record[i][r['time_point']]['so2'] = -1
                if r.has_key('co'):
                    record[i][r['time_point']]['co'] = r['co']
                else:
                    record[i][r['time_point']]['co'] = -1
                if r.has_key('o3'):
                    record[i][r['time_point']]['o3'] = r['o3']
                else:
                    record[i][r['time_point']]['o3'] = -1

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

            if record.has_key(tmp_time) and record[tmp_time]['aqi'] != 0:
                result["aqi"] = record[tmp_time]['aqi']
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
            ofile.write(" %d %d %d %d %d %f %d"%(result["aqi"],result["pm2_5"],result["pm10"],result["no2"],result["so2"],result["co"],result["o3"]))

            ofile.write("\r\n")

            
    ofile.close()

if __name__ == '__main__':
    print "Ready"
    record = get_records()
    time_list = get_time_list('shanghai','low')
    pro_and_write_data(record,'shanghai','low')
    time_list = get_time_list('shanghai','increase')
    pro_and_write_data(record,'shanghai','increase')
    time_list = get_time_list('shanghai','decrease')
    pro_and_write_data(record,'shanghai','decrease')
    time_list = get_time_list('shanghai','high')
    pro_and_write_data(record,'shanghai','high')












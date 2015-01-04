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

stations = ["Haidian"]  
cities = ["Beijing"]
#stations = ["环境监测监理中心","万寿西宫","美国大使馆","官园","定陵","东四","天坛","顺义新城","昌平镇"]  
#cities = ["廊坊","北京","北京","北京","北京","北京","北京","北京","北京"]
#stations = ["海淀区万柳","市环保局","供销社","离宫","市环保局","黑马集团"]  
#cities = ["北京","沧州","唐山","承德","衡水","德州"]

init_time = "2014-01-01T00:00:00Z"
final_time = "2014-10-20T00:00:00Z"


def get_records():
    conn = pymongo.Connection("10.214.0.147",27017)
    db = conn.forecastio
    


    record = [{}]*len(stations)
    for i in range(len(stations)):
        collection = db[cities[i]]
        record[i]={}
        print i
        print stations[i]
        print cities[i]
        tmp_record = collection.find({"position":stations[i]})
        for r in tmp_record:
            record[i][r['date']]=r['hourly']['data']

    return record[0]

def get_time_list(station,mtype):
    ifile=codecs.open(u'../events/'+station+'_'+mtype+'.txt', 'r',"utf-8") 
    tmp_list = ifile.readlines()
    time_list = []
    for t in tmp_list:
        time_list.append(t.strip('\r\n')[0:19] + 'Z')
    return time_list

def pro_and_write_data(record,station,mtype):
    ofile=codecs.open(u'./'+station+'_'+mtype+'1.txt', 'w',"utf-8")
    result = {}
    for current_time in time_list:
        
        unix_current = time.mktime(time.strptime(current_time,ISOTIMEFORMAT))
        for time_iter in range(0,STEP):
            
            unix_tmp = unix_current-time_iter*3600
            tmp_time = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
            print tmp_time

            result["temperature"] = -1
            result["dewPoint"] = -1
            result["humidity"] = -1
            result["cloudCover"] = -1
            result["pressure"] = -1
            result["windSpeed"] = -1
            result["windBearing"] = -1

            time_hourly = string.atoi(tmp_time[11:13])
            '''
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('temperature') and record[tmp_time[0:10]][time_hourly]['temperature'] != 0:
                result["temperature"] = record[tmp_time[0:10]][time_hourly]['temperature']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('dewPoint') and record[tmp_time[0:10]][time_hourly]['dewPoint'] != 0:
                result["dewPoint"] = record[tmp_time[0:10]][time_hourly]['dewPoint']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('humidity') and record[tmp_time[0:10]][time_hourly]['humidity'] != 0:
                result["humidity"] = record[tmp_time[0:10]][time_hourly]['humidity']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('cloudCover') and record[tmp_time[0:10]][time_hourly]['cloudCover'] != 0:
                result["cloudCover"] = record[tmp_time[0:10]][time_hourly]['cloudCover']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('pressure') and record[tmp_time[0:10]][time_hourly]['pressure'] != 0:
                result["pressure"] = record[tmp_time[0:10]][time_hourly]['pressure']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('windSpeed') and record[tmp_time[0:10]][time_hourly]['windSpeed'] != 0:
                result["windSpeed"] = record[tmp_time[0:10]][time_hourly]['windSpeed']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('windBearing') and record[tmp_time[0:10]][time_hourly]['windBearing'] != 0:
                result["windBearing"] = record[tmp_time[0:10]][time_hourly]['windBearing']
            '''
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('temperature'):
                result["temperature"] = record[tmp_time[0:10]][time_hourly]['temperature']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('dewPoint'):
                result["dewPoint"] = record[tmp_time[0:10]][time_hourly]['dewPoint']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('humidity'):
                result["humidity"] = record[tmp_time[0:10]][time_hourly]['humidity']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('cloudCover'):
                result["cloudCover"] = record[tmp_time[0:10]][time_hourly]['cloudCover']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('pressure'):
                result["pressure"] = record[tmp_time[0:10]][time_hourly]['pressure']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('windSpeed') :
                result["windSpeed"] = record[tmp_time[0:10]][time_hourly]['windSpeed']
            if record.has_key(tmp_time[0:10]) and  record[tmp_time[0:10]][time_hourly].has_key('windBearing') :
                result["windBearing"] = record[tmp_time[0:10]][time_hourly]['windBearing']

            ofile.write(tmp_time)
            ofile.write(" %f %f %f %f %f %f %f"%(result["temperature"],result["dewPoint"],result["humidity"],result["cloudCover"],
                                                   result["pressure"],result["windSpeed"],result["windBearing"]))
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
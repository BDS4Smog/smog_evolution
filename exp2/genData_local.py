# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
import time
ISOTIMEFORMAT='%Y-%m-%dT%XZ'
STEP = 6 

STATION = 'haidian'
TYPE = 'decrease'

c = u"海淀区万柳"  ###################### Need to change when changing station ######################
cities = [u"昌平镇",u"奥体中心",u"官园",u"古城"]  ###################### Need to change when changing station ######################

#c = u"官园"  ###################### Need to change when changing station ######################
#cities = [u"古城",u"海淀区万柳",u"奥体中心",u"东四",u"天坛",u"万寿西宫"]  ###################### Need to change when changing station ######################

# = u"古城"  ###################### Need to change when changing station ######################
#cities = [u"昌平镇",u"古城",u"万寿西宫",u"奥体中心"]  ###################### Need to change when changing station ######################

conn = pymongo.Connection("10.214.0.147",27017)

#set database
db = conn.Air
db_weather = conn.forecastio_bj
#db1 = conn.Beijing
#db.authenticate("pm","ccntgrid")
collection = db.Stations
collection_weather = db_weather['Haidian']  ###################### Need to change when changing station ######################
#collection_b = db1.BJ_Weather_Forecast


ofile=codecs.open(u'data/'+STATION+'_'+TYPE+'.txt', 'w',"utf-8")
result = {}
m_result = [{}]*len(cities)
print 'Ready' 
ifile=codecs.open(u'events/'+STATION+'_'+TYPE+'.txt', 'r',"utf-8") ###################### Need to change when changing station ######################
time_list = ifile.readlines()
for current_time in time_list:
    result["pm2_5"]=-1
    result["pm10"]=-1
    result["no2"]=-1
    result["so2"]=-1
    result["co"]=-1
    result["o3"]=-1
    result["temperature"] = -1
    result["dewPoint"] = -1
    result["humidity"] = -1
    result["cloudCover"] = -1
    result["pressure"] = -1
    result["windSpeed"] = -1
    result["windBearing"] = -1
    
    print '-----'
    current_time = current_time.strip('\r\n')[0:19] + 'Z'
    print current_time
    
    unix_current = time.mktime(time.strptime(current_time,ISOTIMEFORMAT))
    for time_iter in range(0,STEP):
        unix_tmp = unix_current-time_iter*3600
        tmp_time = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
        print tmp_time
        record = collection.find({"time_point":tmp_time,"position_name":c,"area":"北京"})
        for r in record:
            if r["pm2_5"]!=0:
                result["pm2_5"] = r["pm2_5"]
            if r["pm10"]!=0:
                result["pm10"] = r["pm10"]
            if r["no2"]!=0:
                result["no2"] = r["no2"]
            if r["so2"]!=0:
                result["so2"] = r["so2"]
            if r["co"]!=0:
                result["co"] = r["co"]
            if r["o3"]!=0:
                result["o3"] = r["o3"]
                
        record = collection_weather.find({"date":tmp_time[0:10]})
        for r in record:
            time_hourly = string.atoi(tmp_time[11:13])
            weather_hourly = r["hourly"]["data"][time_hourly]
            if weather_hourly.has_key("temperature")!=0:
                result["temperature"] = weather_hourly["temperature"]
            if weather_hourly.has_key("dewPoint")!=0:
                result["dewPoint"] = weather_hourly["dewPoint"]
            if weather_hourly.has_key("humidity")!=0:
                result["humidity"] = weather_hourly["humidity"]
            if weather_hourly.has_key("cloudCover")!=0:
                result["cloudCover"] = weather_hourly["cloudCover"]
            if weather_hourly.has_key("pressure")!=0:
                result["pressure"] = weather_hourly["pressure"]
            if weather_hourly.has_key("windSpeed")!=0:
                result["windSpeed"] = weather_hourly["windSpeed"]
            if weather_hourly.has_key("windBearing")!=0:
                result["windBearing"] = weather_hourly["windBearing"]

        for city_iter in range(len(cities)):
            m_result[city_iter]={}
            m_result[city_iter]["pm2_5"]=-1
            m_result[city_iter]["pm10"]=-1
            m_result[city_iter]["no2"]=-1
            m_result[city_iter]["so2"]=-1
            m_result[city_iter]["co"]=-1
            m_result[city_iter]["o3"]=-1
            
            record = collection.find({"time_point":tmp_time,"position_name":cities[city_iter],"area":"北京"})
            for r in record:
                if r["pm2_5"]!=0:
                    m_result[city_iter]["pm2_5"] = r["pm2_5"]
                if r["pm10"]!=0:
                    m_result[city_iter]["pm10"] = r["pm10"]
                if r["no2"]!=0:
                    m_result[city_iter]["no2"] = r["no2"]
                if r["so2"]!=0:
                    m_result[city_iter]["so2"] = r["so2"]
                if r["co"]!=0:
                    m_result[city_iter]["co"] = r["co"]
                if r["o3"]!=0:
                    m_result[city_iter]["o3"] = r["o3"]

        ofile.write(tmp_time)
        ofile.write(" %d %d %d %d %d %d"%(result["pm2_5"],result["pm10"],result["no2"],result["so2"],result["co"],result["o3"]))
        ofile.write(" %f %f %f %f %f %f %f"%(result["temperature"],result["dewPoint"],result["humidity"],result["cloudCover"],
                                                   result["pressure"],result["windSpeed"],result["windBearing"]))
        for city_iter in range(len(cities)):
            ofile.write(" %d %d %d %d %d %d"%(m_result[city_iter]["pm2_5"],m_result[city_iter]["pm10"],m_result[city_iter]["no2"],
                                              m_result[city_iter]["so2"],m_result[city_iter]["co"],m_result[city_iter]["o3"]))
        ofile.write("\r\n")

        
ofile.close()

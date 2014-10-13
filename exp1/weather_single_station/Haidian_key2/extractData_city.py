# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
import time
ISOTIMEFORMAT='%Y-%m-%dT%XZ'

#import math
#connect
c = "海淀区万柳"    ###################### Need to change when changing station ######################
conn = pymongo.Connection("10.214.0.147",27017)
#set database
db = conn.Air
db_weather = conn.forecastio_bj
#db1 = conn.Beijing
#db.authenticate("pm","ccntgrid")
collection = db.Stations
collection_weather = db_weather.Haidian  ###################### Need to change when changing station ######################
#collection_b = db1.BJ_Weather_Forecast

#initialize the tmp result
result = {}
#4 of weather prediction

#select result
print "Ready"

ofile = []              ###################### Need to change when changing station ######################
ofile.append(codecs.open('station_Haidian.txt', 'w',"utf-8"))

distinct_time = collection.distinct('time_point')
current_time = "2014-99-99T"
for i in distinct_time:
    #4 of air pollution
    result["pm2_5"] = -1
    result["temperature"] = -1
    result["dewPoint"] = -1
    result["humidity"] = -1
    result["cloudCover"] = -1
    result["pressure"] = -1
    result["windSpeed"] = -1
    result["windBearing"] = -1
    '''
    result["pm10"] = -1
    result["no2"] = -1
    result["so2"] = -1
    result["co"] = -1
    result["o3"] = -1
    '''
    #4 of pollution 2/3 hours later 
    result["n_pm2_5"] = -1
    '''
    result["n_pm10"] = -1
    result["n_no2"] = -1
    result["n_so2"] = -1
    result["n_co"] = -1
    result["n_o3"] = -1
    result["train"] = -1
    '''
    result["y"] = -1
    result["y1"]=-1
    
    print "-----"
#data for weather pollution
    record = collection.find({"time_point":i,"position_name":c,"area":u"北京"})
    flag1=0
    flag2=0
    for r in record:
        oldtime = i
        newtime_s = time.mktime(time.strptime(oldtime,ISOTIMEFORMAT))+14400
        newtime = time.strftime(ISOTIMEFORMAT,time.localtime(newtime_s))
        record1 = collection.find({"time_point":newtime,"position_name":c,"area":u"北京"})
        
        if(record1.count()!=0):
            result["pm2_5"] = r["pm2_5"]
            '''
            result["pm10"] = r["pm10"]
            result["no2"] = r["no2"]
            result["so2"] = r["so2"]
            result["co"] = r["co"]
            result["o3"] = r["o3"]
            '''
            record2 = collection_weather.find({"date":oldtime[0:10]})
            for r2 in record2:
                
                time_hourly = oldtime[11:13]
                #if(time_hourly[0]=="0"):
                #    time_hourly = time_hourly[1]
                time_hourly = string.atoi(time_hourly)
                weather_hourly = r2["hourly"]["data"][time_hourly]
                if(weather_hourly.has_key("temperature")==0 or weather_hourly.has_key("dewPoint")==0 or weather_hourly.has_key("humidity")==0
                   or weather_hourly.has_key("cloudCover")==0 or weather_hourly.has_key("pressure")==0 or weather_hourly.has_key("windSpeed")==0
                   or weather_hourly.has_key("windBearing")==0):
                    break
                flag2=1
                result["temperature"] = weather_hourly["temperature"]
                result["dewPoint"] = weather_hourly["temperature"]
                result["humidity"] = weather_hourly["humidity"]
                result["cloudCover"] = weather_hourly["temperature"]
                result["pressure"] = weather_hourly["temperature"]
                result["windSpeed"] = weather_hourly["windSpeed"]
                result["windBearing"] = weather_hourly["windBearing"]



                
            for r1 in record1:
                flag1=1
                result["n_pm2_5"] = r1["pm2_5"]
                '''
                result["n_pm10"] = r1["pm10"]
                result["n_no2"] = r1["no2"]
                result["n_so2"] = r1["so2"]
                result["n_co"] = r1["co"]
                result["n_o3"] = r1["o3"]
                '''
                tmp = r["pm2_5"]
                tmp1 = r1["pm2_5"]
                if(tmp<=35):
                    result["y"]=1
                elif(tmp<=75):
                    result["y"]=2
                elif(tmp<=115):
                    result["y"]=3
                elif(tmp<=150):
                    result["y"]=4
                elif(tmp<=250):
                    result["y"]=5
                else:
                    result["y"]=6

                if(tmp1<=35):
                    result["y1"]=1
                elif(tmp1<=75):
                    result["y1"]=2
                elif(tmp1<=115):
                    result["y1"]=3
                elif(tmp1<=150):
                    result["y1"]=4
                elif(tmp1<=250):
                    result["y1"]=5
                else:
                    result["y1"]=6


                if(oldtime[8:10]<="05"):
                    result["train"]=0
                else:
                    result["train"]=1
                break

                
        break

#write to file
    if(flag1==1 and flag2==1 and result["pm2_5"]!=0.0 and result["n_pm2_5"]!=0.0):
        ofile[0].write(oldtime+" "+newtime)
        #write to file
        ofile[0].write(" %f %f %f %f %f %f %f"%(result["temperature"],result["dewPoint"],result["humidity"],result["cloudCover"],
                                                   result["pressure"],result["windSpeed"],result["windBearing"]))
        ofile[0].write(" %d %d %d"%(result["y"],result["y1"],result["train"]))
        ofile[0].write("\r\n")

        print oldtime
        print newtime
        
for i in range(len(ofile)):
    ofile[i].close()


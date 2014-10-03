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
c = "北京"
conn = pymongo.Connection("10.214.0.147",27017)
#set database
db = conn.Air
#db1 = conn.Beijing
#db.authenticate("pm","ccntgrid")
collection = db.Cities
collection_w = db.Weather
#collection_b = db1.BJ_Weather_Forecast

#initialize the tmp result
result = {}
#4 of weather prediction

#select result
print "Ready"

#ofile = codecs.open('X_1', 'w',"utf-8")
ofile1 = codecs.open('city_Beijing.txt', 'w',"utf-8")
distinct_time = collection.distinct('time_point')
current_time = "2014-99-99T"
for i in distinct_time:
    #4 of air pollution
    result["pm2_5"] = -1
    result["pm10"] = -1
    result["no2"] = -1
    result["so2"] = -1
    #4 of weather condition in this time period
    result["wind_direction"] = -1
    result["wind_speed"] = -1
    result["rain_3h"] = -1
    result["clouds"] = -1
    #4 of pollution 2/3 hours later 
    result["n_pm2_5"] = -1
    result["n_pm10"] = -1
    result["n_no2"] = -1
    result["n_so2"] = -1
    result["y"] = -1
    
    
    print "-----"
#data for weather pollution
    record = collection.find({"time_point":i,"area":c})
    flag1=0
    flag2=0
    for r in record:
        oldtime = i
        newtime_s = time.mktime(time.strptime(oldtime,ISOTIMEFORMAT))+7200
        newtime = time.strftime(ISOTIMEFORMAT,time.localtime(newtime_s))
        record1 = collection.find({"time_point":newtime,"area":c})
        if(record1.count()!=0):
            result["pm2_5"] = r["pm2_5"]
            result["pm10"] = r["pm10"]
            result["no2"] = r["no2"]
            result["so2"] = r["so2"]
            for r1 in record1:
                result["n_pm2_5"] = r1["pm2_5"]
                result["n_pm10"] = r1["pm10"]
                result["n_no2"] = r1["no2"]
                flag1=1
                result["n_so2"] = r1["so2"]
                tmp = r["pm2_5"]
                tmp1 = r1["pm2_5"]
                if(oldtime[11:13]<="06"):
                    result["period"]=1
                elif(oldtime[11:13]<="12"):
                    result["period"]=2
                elif(oldtime[11:13]<="18"):
                    result["period"]=3
                else:
                    result["period"]=4
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
                break
        break

#data for weather
#    record = collection_w.find({"time_point":{"$gt": oldtime,"$lt":newtime},"area":c})
#    if(record.count()!=0):
#        flag2=1
#        count = record.count()
#        result["wind_direction"] = 0.0
#        result["wind_speed"] = 0.0
#        result["rain_3h"] = 0.0
#        result["clouds"] = 0.0

#        for r2 in record:
#            result["wind_direction"] += r2["wind_direction_value"]
#            result["wind_speed"] += r2["wind_speed_value"]
#            result["rain_3h"] += r2["rain_3h"]
#            result["clouds"] += r2["clouds_value"]
#        result["wind_direction"] /= count
#        result["wind_speed"] /= count
#        result["rain_3h"] /= count
#        result["clouds"] /= count
        

#write to file
    if(flag1==1):
#        ofile.write(oldtime+" "+newtime)
        
        #write to file
#        ofile.write(" %d %d %f %f %f %f"%(result["period"],result["y"],result["pm2_5"],result["pm10"],result["no2"],result["so2"]))
#        ofile.write(" %f %f %f %f"%(result["wind_direction"],result["wind_speed"],result["rain_3h"],result["clouds"]))  
#        ofile.write(" %f %f %f %f"%(result["n_pm2_5"],result["n_pm10"],result["n_no2"],result["n_so2"]))
#        ofile.write(" %d"%(result["y1"]))
#        ofile.write("\r\n")
        if result["pm2_5"]!=0.0 and result["n_pm2_5"]!=0:
            ofile1.write(oldtime+" "+newtime)
            ofile1.write(" %d %f %d %f %d"%(result["period"],result["pm2_5"],result["y"],result["n_pm2_5"],result["y1"]))
            ofile1.write("\r\n")
        print oldtime
        print newtime
        
ofile1.close()


# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
#import math
#connect
c = "北京"
conn = pymongo.Connection("10.214.0.147",27017)
#set database
db = conn.Air
db1 = conn.Beijing
#db.authenticate("pm","ccntgrid")
collection = db.Cities
collection_w = db.Weather
collection_b = db1.BJ_Weather_Forecast

weather_c = {}
wind_c = {}

tmp = 1
record= collection_b.distinct('tomorrowTianqi')
for i in record:
    weather_c[i]=tmp
    tmp+=1
tmp = 1
record= collection_b.distinct('tomorrowWind')
for i in record:
    wind_c[i]=tmp
    tmp+=1



#initialize the tmp result
result = {}
#4 of weather prediction



#select result
print "Ready"

ofile = codecs.open('Temperal_X_1', 'w',"utf-8")
time = collection.distinct('time_point')
current_time = "2014-99-99T"
for i in time:
    result["weather"] = -1
    result["wind"] = -1
    result["temp_low"] = -1
    result["temp_high"] = -1
    #6 of air pollution
    result["pm2_5"] = -1
    result["pm10"] = -1
    result["no2"] = -1
    result["so2"] = -1
    result["co"] = -1
    result["o3"] = -1
    #4 of weather
    result["humidity"] = -1
    result["wind_speed"] = -1
    result["rain_3h"] = -1
    result["clouds"] = -1
    
    if(i[:11]==current_time):
        continue
    current_time = i[:11]
    print "-----"
    print current_time
#data for weather prediction
    i_s = current_time+"17:30:00Z"
    i_l = current_time+"18:30:00Z"
    record = collection.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})
   
    if(record.count()==0):
        i_s = current_time+"16:30:00Z"
        i_l = current_time+"19:30:00Z"
        record = collection.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})
   
        if(record.count()==0):
            i_s = current_time+"15:30:00Z"
            i_l = current_time+"20:30:00Z"
            record = collection.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})
       
            if(record.count()==0):
                i_s = current_time+"13:30:00Z"
                i_l = current_time+"22:30:00Z"
                record = collection.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})
                print "13"
                print record.count()
    
    t1 = record.count()
   # print t1
    if(t1 == 0):
        result["pm2_5"] = -1
        result["pm10"] = -1
        result["no2"] = -1
        result["so2"] = -1
        result["co"] = -1
        result["o3"] = -1
    else:
        result["pm2_5"] = 0.0
        result["pm10"] = 0.0
        result["no2"] = 0.0
        result["so2"] = 0.0
        result["co"] = 0.0
        result["o3"] = 0.0
        for t2 in record:
            result["pm2_5"] += t2["pm2_5"]
            result["pm10"] += t2["pm10"]
            result["no2"] += t2["no2"]
            result["so2"] += t2["so2"]
            result["co"] += t2["co"]
            result["o3"] += t2["o3"]
        result["pm2_5"] /= t1
        result["pm10"] /= t1
        result["no2"] /= t1
        result["so2"] /= t1
        result["co"] /= t1
        result["o3"] /= t1
#data for air pollution
    i_s = current_time+"17:30:00Z"
    i_l = current_time+"18:30:00Z"
    record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})
    if(record.count()==0):
        i_s = current_time+"16:30:00Z"
        i_l = current_time+"19:30:00Z"
        record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})

        if(record.count()==0):
            i_s = current_time+"15:30:00Z"
            i_l = current_time+"20:30:00Z"
            record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})
 
            if(record.count()==0):
                i_s = current_time+"13:30:00Z"
                i_l = current_time+"22:30:00Z"
                record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":c})
              #  print c+"23"+" "
              #  print record.count()

    t1 = record.count()
    #print t1
    if(t1 == 0):
        result["humidity"] = -1
        result["wind_speed"] = -1
        result["rain_3h"] = -1
        result["clouds"] = -1
    else:
        result["humidity"] = 0.0
        result["wind_speed"] = 0.0
        result["rain_3h"] = 0.0
        result["clouds"] = 0.0

        for t2 in record:
            result["humidity"] += t2["humidity"]
            result["wind_speed"] += t2["wind_speed_value"]
            result["rain_3h"] += t2["rain_3h"]
            result["clouds"] += t2["clouds_value"]
        result["humidity"] /= t1
        result["wind_speed"] /= t1
        result["rain_3h"] /= t1
        result["rain_3h"] += 1   #!!!!!!!!!!!!
        result["clouds"] /= t1
#data for weather
    current_t = current_time[0:4]+"."+current_time[5:7]+"."+current_time[8:10]
    record = collection_b.find({"time":current_t,"period":"晚"})
    for i in record:
        print "------"+i["tomorrowTianqi"]
        result["weather"] = weather_c[i["tomorrowTianqi"]]
        print result["weather"]
        result["wind"] = wind_c[i["tomorrowWind"]]
        result["temp_low"] = string.atoi(i["tomorrowTempMin"])
        result["temp_high"] = string.atoi(i["tomorrowTempMax"])

#    for i in result:
#        print i
#        print result[i]

#    os.system("pause")

#write to file
    ofile.write(current_time+"18:00:00Z"+" ")
    #write to file
    
    ofile.write(" %d %d %d %d"%(result["weather"],result["wind"],result["temp_low"],result["temp_high"]))
    ofile.write(" %f %f %f %f %f %f"%(result["pm2_5"],result["pm10"],result["no2"],result["so2"],result["co"],result["o3"]))
    ofile.write(" %f %f %f %f"%(result["humidity"],result["wind_speed"],result["rain_3h"],result["clouds"]))  
    ofile.write("\r\n")
ofile.close()
#result = collection.find({"area":"舟山","aqi":{"$gte":300}})
#for i in result:
#    print i


'''
collection = db.City

#insert
#user = {"name":"zyl","age":"10"}
#collection.insert(user)
#users = [{"name":"jz","age":"11"},{"name":"az"}]
#collection.insert(users)

#select
#print collection.find_one()
#for data in collection.find():
#    print data
#print collection.count()  
#for data in collection.find({"name":"zyl"}):  
#    print data
#for data in collection.find({"age":{"$gt":"10"}}).sort("age"):  
#    print data

#query
#print db.collection_names()

#initialize the array result


result = {}
for content in collection.find():
    tmp = {}
    tmp["count"]=0
    tmp["count_all"]=0
    result[content["area"]]=tmp


#get the count    
collection = db.Cities
t = 1
for i in result:
    result[i]["count"] = collection.find({"area":i,"aqi":{"$gte":300}}).count()
    result[i]["count_all"] = collection.find({"area":i}).count()
    result[i]["ratio"]=float(result[i]["count"])/result[i]["count_all"]
    print i
    print t
    t+=1
#sort 
result = sorted(result.items(),lambda x,y:cmp(x[1]["ratio"],y[1]["ratio"]),reverse=True)
#output to file agi_gt_300.txt
ofile = codecs.open('aqi_gt_300.csv', 'w',"utf-8")
for i in range(len(result)):
    ofile.write(result[i][0]+",%d,%d,%f\r\n"%(result[i][1]["count"],result[i][1]["count_all"],result[i][1]["ratio"]));

  
ofile.close()
'''

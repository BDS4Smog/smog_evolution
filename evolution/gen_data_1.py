# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import string
import codecs
#import math
#connect
conn = pymongo.Connection("10.214.0.147",27017)
#set database
db = conn.Air
#db.authenticate("pm","ccntgrid")
#set collection
collection = db.City

#get all city name
city = collection.find()

#initialize the tmp result
result = {}
for i in city:
    name = i["area"]
    result[name] = {}
    result[name][0] = -1 #means pm2_6
    result[name][1] = -1 #means pm10
#    result[name][2] = -1 #means pm10
    result[name][2] = -1
    result[name][3] = -1


#select result
collection = db.Cities
collection_w = db.Weather

ofile = codecs.open('city_num_X_1', 'w',"utf-8")
count = 1
for tmp in result:
    ofile.write(tmp+" %d\r\n"%(count))
    count+=1
ofile.close()

print "Ready"

ofile = codecs.open('X_1', 'w',"utf-8")
time = collection.distinct('time_point')
current_time = "2014-99-99T"
for i in time:
    if(i[:11]==current_time):
        continue
    current_time = i[:11]
    print "-----"
    print current_time
    record = collection.find({"time_point":current_time+"18:00:00Z"})
    for t in record:
        city = t["area"]
        result[city][0] = t["pm2_5"]
        result[city][1] = t["pm10"]

    
    i_s = i[:11]+"17:30:00Z"
    i_l = i[:11]+"18:30:00Z"
    record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l}})
    for t in record:
        city = t["area"]
        result[city][2] = t["wind_direction_value"]
        result[city][3] = t["wind_speed_value"]
        
 
    ofile.write(current_time+"18:00:00Z"+" ")
    #write to file
    for city in result:
        #check if the result is empty
        #data in cities
        if(result[city][0]==-1):
            i_s = current_time+"16:30:00Z"
            i_l = current_time+"19:30:00Z"
            record = collection.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":city})
       
            if(record.count()==0):
                i_s = current_time+"15:30:00Z"
                i_l = current_time+"20:30:00Z"
                record = collection.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":city})
           
                if(record.count()==0):
                    i_s = current_time+"13:30:00Z"
                    i_l = current_time+"22:30:00Z"
                    record = collection.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":city})
                    print city+"13"+" "
            t1 = record.count()
           # print t1
            if(t1 != 0):
                result[city][0] = 0.0
                result[city][1] = 0.0
                for t2 in record:
                    result[city][0] = result[city][0]+t2["pm2_5"]
                    result[city][1] = result[city][1]+t2["pm10"]
                
                result[city][0]=result[city][0]/t1
                result[city][1]=result[city][1]/t1

        if(result[city][2]==-1):
            i_s = i[:11]+"16:30:00Z"
            i_l = i[:11]+"19:30:00Z"
            record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":city})
  
            if(record.count()==0):
                i_s = i[:11]+"15:30:00Z"
                i_l = i[:11]+"20:30:00Z"
                record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":city})
     
                if(record.count()==0):
                    i_s = i[:11]+"13:30:00Z"
                    i_l = i[:11]+"22:30:00Z"
                    record = collection_w.find({"time_point":{"$gt": i_s,"$lt":i_l},"area":city})
            t1 = record.count()
            #print t1
            if(t1 != 0):
                result[city][2]=0
                result[city][3]=0
                for t2 in record:
                    result[city][2] = result[city][2]+t2["wind_direction_value"]
                    result[city][3] = result[city][3]+t2["wind_speed_value"]
                result[city][2]=result[city][2]/t1
                result[city][3]=result[city][3]/t1
            
        ofile.write(" %d %d %f %f "%(result[city][0],result[city][1],result[city][2],result[city][3]));      
        result[city][0]=-1
        result[city][1]=-1
        result[city][2]=-1
        result[city][3]=-1
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

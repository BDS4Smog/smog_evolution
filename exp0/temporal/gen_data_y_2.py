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
    result[name] = -1 #aqi>200

#select result
collection = db.Cities

ofile = codecs.open('city_num_y_1', 'w',"utf-8")
count = 1
for tmp in result:
    ofile.write(tmp+" %d\r\n"%(count))
    count+=1
ofile.close()

print "Ready"

ofile = codecs.open('y_1_test_1', 'w',"utf-8")
time = collection.distinct('time_point')
tmp
current_time = "2014-99-99T"
present_time = "2014-99-99T"
for i in time:
    if(i[:11]==current_time):
#    if(i[11]!='1' or i[12]!='8'):
        continue
    print "---"
    present_time = current_time
    current_time = i[:11]
        
    i_s = current_time+"18:00:00Z"
    i_l = present_time+"17:59:59Z"

    print i_s
    print i_l
    
    record = collection.find({"time_point":{"$gte": i_s,"$lt":i_l}})
    
#    print i
    old_time = "2014-99-13T18:00:00Z"
    old_area = "ss"
    for t in record:
        t_name = t["area"]
        if (result[t_name] == -1):
            result[t_name]=0
            
        if(t["aqi"]>200 and (t["time_point"]!=old_time or t["area"]!=old_time)):
            old_time = t["time_point"]
            old_area = t["area"]
#            result[t_name]+=1
            result[t_name]=1       
    ofile.write(current_time)
    print current_time
    for tmp in result:
#        if (result[tmp]>0 and result[tmp]<2):
#            result[tmp]=0
#        elif(result[tmp]>=2):
#            result[tmp]=1
        ofile.write(" %d"%(result[tmp]));
        result[tmp] = -1
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

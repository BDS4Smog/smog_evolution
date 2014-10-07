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
c = "东四"
cities = [u"昌平镇",u"古城",u"万寿西宫",u"奥体中心"]



conn = pymongo.Connection("10.214.0.147",27017)
#set database
db = conn.Air
#db1 = conn.Beijing
#db.authenticate("pm","ccntgrid")
collection = db.Stations
#collection_b = db1.BJ_Weather_Forecast

#initialize the tmp result
result = {}
#4 of weather prediction

#select result
print "Ready"

ofile = []
ofile.append(codecs.open('station_Dongsi.txt', 'w',"utf-8"))
ofile.append(codecs.open('station_Dongsi_1.txt', 'w',"utf-8"))
ofile.append(codecs.open('station_Dongsi_2.txt', 'w',"utf-8"))
ofile.append(codecs.open('station_Dongsi_3.txt', 'w',"utf-8"))
ofile.append(codecs.open('station_Dongsi_4.txt', 'w',"utf-8"))
ofile.append(codecs.open('station_Dongsi_5.txt', 'w',"utf-8"))
ofile.append(codecs.open('station_Dongsi_6.txt', 'w',"utf-8"))

distinct_time = collection.distinct('time_point')
current_time = "2014-99-99T"
tmp_result = []
for i in range(len(cities)):
    tmp_dic = {}
    tmp_dic["pm2_5"] = 0.0
    tmp_dic["pm10"] = 0.0
    tmp_dic["no2"] = 0.0
    tmp_dic["so2"] = 0.0
    tmp_dic["co"] = 0.0
    tmp_dic["o3"] = 0.0
    tmp_result.append(tmp_dic)
    
for i in distinct_time:
    #4 of air pollution
    result["pm2_5"] = -1
    result["pm10"] = -1
    result["no2"] = -1
    result["so2"] = -1
    result["co"] = -1
    result["o3"] = -1
    #4 of pollution 2/3 hours later 
    result["n_pm2_5"] = -1
    result["n_pm10"] = -1
    result["n_no2"] = -1
    result["n_so2"] = -1
    result["n_co"] = -1
    result["n_o3"] = -1
    result["train"] = -1
    result["y"] = -1
    result["y1"]=-1
    
    print "-----"
#data for weather pollution
    record = collection.find({"time_point":i,"position_name":c})
    flag1=0
    if(record.count()==0):
        continue
    for r in record:
        avg_result = {}
        avg_count = {}
        avg_result["pm2_5"] = 0.0
        avg_result["pm10"] = 0.0
        avg_result["no2"] = 0.0
        avg_result["so2"] = 0.0
        avg_result["co"] = 0.0
        avg_result["o3"] = 0.0
        avg_count["pm2_5"] = 0
        avg_count["pm10"] = 0
        avg_count["no2"] = 0
        avg_count["so2"] = 0
        avg_count["co"] = 0
        avg_count["o3"] = 0
        
        oldtime = i
        newtime_s = time.mktime(time.strptime(oldtime,ISOTIMEFORMAT))+7200
        newtime = time.strftime(ISOTIMEFORMAT,time.localtime(newtime_s))
        record1 = collection.find({"time_point":newtime,"position_name":c})
        if(record1.count()!=0):
            result["pm2_5"] = r["pm2_5"]
            print r["pm2_5"]
            if(r["pm2_5"]!=0):
                avg_result["pm2_5"]+=r["pm2_5"]
                avg_count["pm2_5"]+=1
            result["pm10"] = r["pm10"]
            if(r["pm10"]!=0):
                avg_result["pm10"]+=r["pm10"]
                avg_count["pm10"]+=1
            result["no2"] = r["no2"]
            if(r["no2"]!=0):
                avg_result["no2"]+=r["no2"]
                avg_count["no2"]+=1
            result["so2"] = r["so2"]
            if(r["so2"]!=0):
                avg_result["so2"]+=r["so2"]
                avg_count["so2"]+=1
            result["co"] = r["co"]
            if(r["co"]!=0):
                avg_result["co"]+=r["co"]
                avg_count["co"]+=1
            result["o3"] = r["o3"]
            if(r["o3"]!=0):
                avg_result["o3"]+=r["o3"]
                avg_count["o3"]+=1
            for r1 in record1:
                flag1=1
                result["n_pm2_5"] = r1["pm2_5"]
                result["n_pm10"] = r1["pm10"]
                result["n_no2"] = r1["no2"]
                result["n_so2"] = r1["so2"]
                result["n_co"] = r1["co"]
                result["n_o3"] = r1["o3"]
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

                for i_c in range(len(cities)):
                    record2 = collection.find({"time_point":oldtime,"position_name":cities[i_c],"area":u"北京"})
                    if(record2.count()==0):
                        flag1=0
                        break
                    for r2 in record2:
                        tmp_result[i_c]["pm2_5"] = r2["pm2_5"]
                        print r2["pm2_5"]
                        print oldtime
                        if(r2["pm2_5"]!=0):
                            avg_result["pm2_5"]+=r2["pm2_5"]
                            avg_count["pm2_5"]+=1
                        tmp_result[i_c]["pm10"] = r2["pm10"]
                        if(r2["pm10"]!=0):
                            avg_result["pm10"]+=r2["pm10"]
                            avg_count["pm10"]+=1
                        tmp_result[i_c]["no2"] = r2["no2"]
                        if(r2["no2"]!=0):
                            avg_result["no2"]+=r2["no2"]
                            avg_count["no2"]+=1
                        tmp_result[i_c]["so2"] = r2["so2"]
                        if(r2["so2"]!=0):
                            avg_result["so2"]+=r2["so2"]
                            avg_count["so2"]+=1
                        tmp_result[i_c]["co"] = r2["co"]
                        if(r2["co"]!=0):
                            avg_result["co"]+=r2["co"]
                            avg_count["co"]+=1
                        tmp_result[i_c]["o3"] = r2["o3"]
                        if(r2["o3"]!=0):
                            avg_result["o3"]+=r2["o3"]
                            avg_count["o3"]+=1
                        break

                break

                
        break
 

    
#write to file
    if(flag1==1 and result["pm2_5"]!=0 and result["n_pm2_5"]!=0 and avg_count["pm2_5"]!=0 and avg_count["pm10"]!=0 and avg_count["no2"]!=0 and avg_count["so2"]!=0 and avg_count["co"]!=0 and avg_count["o3"]!=0):

        avg_result["pm2_5"] = avg_result["pm2_5"]/avg_count["pm2_5"]
        avg_result["pm10"] = avg_result["pm10"]/avg_count["pm10"]
        avg_result["no2"] = avg_result["no2"]/avg_count["no2"]
        avg_result["so2"] = avg_result["so2"]/avg_count["so2"]
        avg_result["co"] = avg_result["co"]/avg_count["co"]
        avg_result["o3"] = avg_result["o3"]/avg_count["o3"]
        if(result["pm2_5"]==0):
            result["pm2_5"]=avg_result["pm2_5"]
        if(result["pm10"]==0):
            result["pm10"]=avg_result["pm10"]
        if(result["no2"]==0):
            result["no2"]=avg_result["no2"]
        if(result["so2"]==0):
            result["so2"]=avg_result["so2"]
        if(result["co"]==0):
            result["co"]=avg_result["co"]
        if(result["o3"]==0):
            result["o3"]=avg_result["o3"]
        for i_c in range(len(cities)):
            if(tmp_result[i_c]["pm2_5"]==0):
                tmp_result[i_c]["pm2_5"]=avg_result["pm2_5"]
            if(tmp_result[i_c]["pm10"]==0):
                tmp_result[i_c]["pm10"]=avg_result["pm10"]
            if(tmp_result[i_c]["no2"]==0):
                tmp_result[i_c]["no2"]=avg_result["no2"]
            if(tmp_result[i_c]["so2"]==0):
                tmp_result[i_c]["so2"]=avg_result["so2"]
            if(tmp_result[i_c]["co"]==0):
                tmp_result[i_c]["co"]=avg_result["co"]
            if(tmp_result[i_c]["o3"]==0):
                tmp_result[i_c]["o3"]=avg_result["o3"]
        
        ofile[0].write(oldtime+" "+newtime)
        #write to file
        ofile[0].write(" %f %f %f %f %f %f"%(result["pm2_5"],result["pm10"],result["no2"],result["so2"],result["co"],result["o3"]))
        for i_c in range(len(cities)):
            ofile[0].write(" %f %f %f %f %f %f"%(tmp_result[i_c]["pm2_5"],tmp_result[i_c]["pm10"],tmp_result[i_c]["no2"],tmp_result[i_c]["so2"],tmp_result[i_c]["co"],tmp_result[i_c]["o3"]))
        ofile[0].write(" %d %d %d"%(result["y"],result["y1"],result["train"]))
        ofile[0].write("\r\n")

        tmp = result["y"]
        ofile[tmp].write(oldtime+" "+newtime)
        ofile[tmp].write(" %f %f %f %f %f %f"%(result["pm2_5"],result["pm10"],result["no2"],result["so2"],result["co"],result["o3"]))
        for i_c in range(len(cities)):
            ofile[tmp].write(" %f %f %f %f %f %f"%(tmp_result[i_c]["pm2_5"],tmp_result[i_c]["pm10"],tmp_result[i_c]["no2"],tmp_result[i_c]["so2"],tmp_result[i_c]["co"],tmp_result[i_c]["o3"]))
        ofile[tmp].write(" %d %d %d"%(result["y"],result["y1"],result["train"]))
        ofile[tmp].write("\r\n")
        print oldtime
        print newtime
        
for i in range(len(ofile)):
    ofile[i].close()


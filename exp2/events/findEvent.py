# -*- coding: utf-8 -*-
import pymongo
import sys
import datetime
import codecs

HOST = '10.214.0.147'
PORT = 27017
DB_NAME = 'Air'
C_NAME = 'Stations'
CITY = '北京'
IN_HOURS_BEFORE = 2 
IN_HOURS_AFTER = 6 
DE_HOURS_BEFORE = 6 
DE_HOURS_AFTER = 2 
LEVEL = 150
START_TIME = '2013-12-25T00:00:00Z'
END_TIME = '2014-10-29T00:00:00Z'
STEP = 6

def strToDatetime(s):
    year = int(s[0:4])
    month = int(s[5:7])
    day = int(s[8:10])
    hour = int(s[11:13])
    return datetime.datetime(year,month,day,hour)

def dataFromMongo(position):
    conn = pymongo.Connection(HOST,PORT)
    db = conn[DB_NAME]
    c = db[C_NAME]
    records = c.find({"position_name":position,"area":CITY})
    t_aqi = {}
    for r in records:
        time_point = r['time_point']
        aqi = r['aqi']
        if aqi > 0:
            print time_point + ': ' + str(aqi)
            t_aqi[time_point[0:19]]=aqi
    conn.close()
    return t_aqi

def checkTime_increase(t_aqi,hour_i):

    if t_aqi.has_key(hour_i.isoformat())==False:
        return False

    if t_aqi[hour_i.isoformat()]>=LEVEL:
        return False

    hour_after = hour_i + datetime.timedelta(0,3600)
    if t_aqi.has_key(hour_after.isoformat()) and t_aqi[hour_after.isoformat()]<LEVEL:
        return False

    hour_before = hour_i - datetime.timedelta(0,3600)
    if t_aqi.has_key(hour_before.isoformat()) and t_aqi[hour_before.isoformat()]>=LEVEL:
        return False

    count1 = 0
    count2 = 0
    for j in range(1,IN_HOURS_AFTER+1):
        hour = hour_i + datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat())==False or t_aqi[hour.isoformat()]>=LEVEL:
            count1 = count1 + 1 
        if t_aqi.has_key(hour.isoformat()):
            count2 = count2 + 1
    if count1 <= IN_HOURS_AFTER - 1:
        return False
    if count2 < IN_HOURS_AFTER/2:
        return False

    count1 = 0
    count2 = 0
    for k in range(1,IN_HOURS_BEFORE+1):
        hour = hour_i - datetime.timedelta(0,3600*k)
        if t_aqi.has_key(hour.isoformat())==False or t_aqi[hour.isoformat()]<LEVEL:
            count1 = count1 + 1
        if t_aqi.has_key(hour.isoformat()):
            count2 = count2 + 1
    if count1 <= IN_HOURS_BEFORE - 1:
        return False
    if count2 < IN_HOURS_BEFORE/2:
        return False

    return True 

def checkTime_decrease(t_aqi,hour_i):
    if t_aqi.has_key(hour_i.isoformat())==False:
        return False

    if t_aqi[hour_i.isoformat()]<LEVEL:
        return False

    hour_after = hour_i + datetime.timedelta(0,3600)
    if t_aqi.has_key(hour_after.isoformat()) and t_aqi[hour_after.isoformat()]>=LEVEL:
        return False
    
    hour_before = hour_i - datetime.timedelta(0,3600)
    if t_aqi.has_key(hour_before.isoformat()) and t_aqi[hour_before.isoformat()]<LEVEL:
        return False

    count1 = 0
    count2 = 0
    for j in range(1,DE_HOURS_AFTER+1):
        hour = hour_i + datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat()) == False or t_aqi[hour.isoformat()]<LEVEL:
            count1 = count1 + 1 
        if t_aqi.has_key(hour.isoformat()):
            count2 = count2 + 1
    if count1 <= DE_HOURS_AFTER - 1:
        return False
    if count2 < DE_HOURS_AFTER/2:
        return False

    count1 = 0
    count2 = 0
    for k in range(1,DE_HOURS_BEFORE+1):
        hour = hour_i - datetime.timedelta(0,3600*k)
        if t_aqi.has_key(hour.isoformat()) == False or t_aqi[hour.isoformat()]>=LEVEL:
            count1 = count1 + 1
        if t_aqi.has_key(hour.isoformat()):
            count2 = count2 + 1
    if count1 <= DE_HOURS_BEFORE - 1:
        return False
    if count2 < DE_HOURS_BEFORE/2:
        return False

    if hour_i.isoformat()=='2014-10-25T17:00:00':
        print 'c'

    return True

def saveFile(file_name,lines):
    f=codecs.open(file_name,'w','utf-8')
    f.writelines(lines)
    f.close()

def eventExtend(hour_i,eventType,t_aqi):
    e_hours = [hour_i.isoformat()+'\r\n']
    for k in range(1,STEP):
        hour = hour_i - datetime.timedelta(0,3600*k)
        if t_aqi.has_key(hour.isoformat()) and eventType=='increase' and t_aqi[hour.isoformat()]<LEVEL:
            e_hours.append(hour.isoformat()+'\r\n')    
        if t_aqi.has_key(hour.isoformat()) and eventType=='decrease' and t_aqi[hour.isoformat()]>=LEVEL:
            e_hours.append(hour.isoformat()+'\r\n')    
    return e_hours

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: python findEvent.py increase/decrease station'
        sys.exit(0)
    eventType = sys.argv[1]
    position = sys.argv[2]
    fileName = position + '_' + eventType + '.txt'
    print 'get data from mongo ...'
    t_aqi = dataFromMongo(position)
    print 'find events ...'
    hour_i = strToDatetime(START_TIME)
    hours = []
    while hour_i.isoformat() <= END_TIME:
        tag = False
        if eventType=='increase':
            tag = checkTime_increase(t_aqi,hour_i)
        if eventType=='decrease':
            tag = checkTime_decrease(t_aqi,hour_i)
        if tag:
            e_hours = eventExtend(hour_i,eventType,t_aqi)
            hours.extend(e_hours)
        hour_i = hour_i + datetime.timedelta(0,3600)
    print 'save hours to file ...'
    saveFile(fileName, hours)


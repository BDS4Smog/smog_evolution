# -*- coding: utf-8 -*-
import pymongo
import sys
import datetime
import codecs

HOST = '10.214.0.147'
PORT = 27017
DB_NAME = 'Air'
C_NAME = 'Cities'
CITY = '上海'
IN_HOURS_BEFORE = 8 
IN_HOURS_AFTER = 10 
DE_HOURS_BEFORE = 8 
DE_HOURS_AFTER = 10 
AQI_LEVEL = 150
START_TIME = '2013-05-28T00:00:00'
END_TIME = '2014-11-30T23:00:00'
STEP = 12
POSITION={'haidian':'海淀区万柳','gucheng':'古城'}

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
    if position == '':
        records = c.find({"area":CITY})
    else:
        records = c.find({"position_name":position,"area":CITY})
    t_aqi = {}
    for r in records:
        time_point = r['time_point']
        aqi = r['aqi']
        if aqi > 0:
            t_aqi[time_point[0:19]]=aqi
    conn.close()
    return t_aqi

def aqiFit(t_aqi):
    aqi = {} 
    hour_i = strToDatetime(START_TIME)
    while hour_i.isoformat() <= END_TIME:
        s = hour_i.isoformat()
        if t_aqi.has_key(s):
            aqi[s]=t_aqi[s]
        else:
            h_b = hour_i - datetime.timedelta(0,3600)
            h_a = hour_i + datetime.timedelta(0,3600)
            s_b = h_b.isoformat()
            s_a = h_a.isoformat()
            if t_aqi.has_key(s_b) and t_aqi.has_key(s_a):
                aqi[s] = (t_aqi[s_a]+t_aqi[s_b])/2
        hour_i = hour_i + datetime.timedelta(0,3600)
    return aqi



def isIncrease(t_aqi,hour_i):
    for j in range(1,IN_HOURS_AFTER+1):
        hour = hour_i + datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat())==False or t_aqi[hour.isoformat()]<AQI_LEVEL:
            return False
    for k in range(0,IN_HOURS_BEFORE):
        hour = hour_i - datetime.timedelta(0,3600*k)
        if t_aqi.has_key(hour.isoformat())==False or t_aqi[hour.isoformat()]>=AQI_LEVEL:
            return False
    return True 

def isDecrease(t_aqi,hour_i):
    for j in range(1,DE_HOURS_AFTER+1):
        hour = hour_i + datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat()) == False or t_aqi[hour.isoformat()]>=AQI_LEVEL:
            return False
    for k in range(0,DE_HOURS_BEFORE):
        hour = hour_i - datetime.timedelta(0,3600*k)
        if t_aqi.has_key(hour.isoformat()) == False or t_aqi[hour.isoformat()]<AQI_LEVEL:
            return False
    return True

def saveFile(file_name,lines):
    f=codecs.open(file_name,'w','utf-8')
    f.writelines(lines)
    f.close()

def eventExtend(hour_i,t,t_aqi):
    e_hours = []
    for k in range(0,STEP):
        hour = hour_i - datetime.timedelta(0,3600*k)
        s = hour.isoformat()
        if t_aqi.has_key(s):
            if (t=='increase' and t_aqi[s]<AQI_LEVEL) or (t=='decrease' and t_aqi[s]>=AQI_LEVEL):
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
    if position == 'shanghai':
        t_aqi = dataFromMongo('')
    else:
        t_aqi = dataFromMongo(POSITION[position])
    t_aqi = aqiFit(t_aqi)
    print 'find events ...'
    hour_i = strToDatetime(START_TIME)
    hours = []
    while hour_i.isoformat() <= END_TIME:
        s = hour_i.isoformat()
        if t_aqi.has_key(s):
            print s + ' ' + str(t_aqi[s])
        if (eventType=='increase' and isIncrease(t_aqi,hour_i)) or (eventType=='decrease' and isDecrease(t_aqi,hour_i)):
            e_hours = eventExtend(hour_i,eventType,t_aqi)
            hours.extend(e_hours)
        hour_i = hour_i + datetime.timedelta(0,3600)
    print 'save hours to file ...'
    saveFile(fileName, hours)


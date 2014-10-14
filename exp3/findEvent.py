import pymongo
import sys
import datetime

HOST = '10.214.0.147'
PORT = 27017
DB_NAME = 'Air'
C_NAME = 'Stations'
CITY = '北京'
HOURS_BEFORE = 8
BETA1 = 2
HOURS_AFTER = 8
BETA2 = 2
ALPHA = 150
START_TIME = '2013-05-01T00:00:00Z'
END_TIME = '2014-10-13T00:00:00Z'

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
    records = c.find({"time_point":{"$gte":START_TIME,"$lte":END_TIME},"position_name":c,"area":CITY})
    t_aqi = {}
    for r in records:
        t_aqi[r['time_point']]=r['aqi']
    return t_aqi

def checkTime_increase(t_aqi,hour_i):
    if !t_aqi.has_key(hour_i.isoformat()+'Z'):
        return False
    count1 = 0
    for j in range(1,HOURS_AFTER):
        hour = hour_i + datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat()+'Z') and t_aqi[hour.isoformat()+'Z']<150:
            count1 = count1 + 1 
    if count1 > BETA1:
        return False
    count2 = 0
    for k in range(0,HOURS_BEFORE):
        hour = hour_i - datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat()+'Z') and t_aqi[hour.isoformat()+'Z']>=150:
            count2 = count2 + 1
    if count2 > BETA2:
        return False
    return True

def checkTime_decrease(t_aqi,hour_i):
    if !t_aqi.has_key(hour_i.isoformat()+'Z'):
        return False
    count1 = 0
    for j in range(0,HOURS_AFTER):
        hour = hour_i + datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat()+'Z') and t_aqi[hour.isoformat()+'Z']>=150:
            count1 = count1 + 1 
    if count1 > BETA1:
        return False
    count2 = 0
    for k in range(1,HOURS_BEFORE):
        hour = hour_i - datetime.timedelta(0,3600*j)
        if t_aqi.has_key(hour.isoformat()+'Z') and t_aqi[hour.isoformat()+'Z']<150:
            count2 = count2 + 1
    if count2 > BETA2:
        return False
    return True

def saveFile(file_name,lines):
    f=open(file_name,'w')
    f.writelines(lines)
    f.close()

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print 'usage: python findEvent.py type station'
    eventType = sys.argv[0]
    position = sys.argv[1]
    fileName = 'hours_' + position + '_' + eventType + '.txt'
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
            hours.append(hour_i.isoformat()+'\r\n')
        hour_i = hour_i + datetime.timedelta(0,3600)
    print 'save hours to file ...'
    saveFile(fileName, hours)


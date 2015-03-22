import sys
import codecs
import time
import datetime

ISOTIMEFORMAT='%Y-%m-%dT%XZ'
STEP = 24 
START_TIME = '2013-05-28T00:00:00'
END_TIME = '2014-12-31T03:00:00'
AQI_LEVEL = 150

def strToDatetime(s):
    year = int(s[0:4])
    month = int(s[5:7])
    day = int(s[8:10])
    hour = int(s[11:13])
    return datetime.datetime(year,month,day,hour)

def readFile(file_name):
    f=codecs.open(file_name,'r','utf-8')
    lines = f.readlines()
    f.close()
    return lines

def readTAQI(file_name):
    lines = readFile(file_name)
    t_aqi = {} 
    for line in lines:
        tmp = line.strip().split(' ')
        t_aqi[tmp[0]] = int(tmp[1])
    return t_aqi

def readTime(file_name):
    lines = readFile(file_name)
    hours = []
    for line in lines:
        hours.append(line.strip() + 'Z')
    return hours

def saveFile(file_name,lines):
    f=codecs.open(file_name,'w','utf-8')
    f.writelines(lines)
    f.close()

def isHigh(hour_i,t_aqi):
    for k in range(0,STEP + 2): 
        hour = hour_i + datetime.timedelta(0,3600*k)
        if t_aqi.has_key(hour.isoformat())==False or t_aqi[hour.isoformat()] < (AQI_LEVEL+20):
            return False
    return True

def isLow(hour_i,t_aqi):
    for k in range(0,STEP + 4): 
        hour = hour_i + datetime.timedelta(0,3600*k)
        if t_aqi.has_key(hour.isoformat())==False or t_aqi[hour.isoformat()] >= (AQI_LEVEL-30):
            return False
    return True


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: python findEvent.py low/high station'
        sys.exit(0)
    eventType = sys.argv[1]
    station = sys.argv[2]
    t_aqi = readTAQI(station + '_records.txt')
    hour_i = strToDatetime(START_TIME)
    hours = []
    while hour_i.isoformat() <= END_TIME:
        if (eventType == 'low' and isLow(hour_i,t_aqi)) or (eventType == 'high' and isHigh(hour_i,t_aqi)):
            hours.append(hour_i.isoformat() + '\r\n')
        hour_i = hour_i + datetime.timedelta(0,3600)

    saveFile(station + '_' + eventType + '.txt',hours)

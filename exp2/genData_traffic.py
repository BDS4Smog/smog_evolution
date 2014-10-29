# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import time

DB_NAME = 'CityWeibo_API'
C_NAME = 'beijing'
HOST = '10.214.0.147'
PORT = 27017
ISOTIMEFORMAT='%Y-%m-%dT%XZ'
STEP = 6
DELT_T = 12
EDGE = 0.2
C_LAT = 39.87275
C_LON = 116.3057

WORDS = [u'堵车',u'塞车']

def getTime(file_name):
    f = open(file_name)
    lines = f.readlines()
    f.close()
    T = []
    for line in lines:
        T.append(line.strip()+'Z')
    return T

def expendTime(T):
    eT = []
    for t in T:
        unix_current = time.mktime(time.strptime(t,ISOTIMEFORMAT)) 
        for i in range(0,STEP):
            unix_tmp = unix_current-i*3600
            tmp_time = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
            eT.append(tmp_time)    
    return eT

def saveFile(lines,file_name)
    f = open(file_name)
    f.writelines(lines)
    f.close()

def tweet_filter(t,c):
    traffic_num = 0
    tweet_num = 0
    q_s = '.*' + num2month(t[5:7]) + ' ' + t[8:10] + '.*' + t[0:4]
    records = c.find({'created_at':{'$regex':q_s}})
    for r in records:
        text = r['text']
        created_at = r['created_at']
        lat = r['geo']['coordinates'][0]
        lon = r['geo']['coordinates'][1]
        if inTime(created_at,t) and inArea(lat,lon):
            tweet_num += 1
            if hasKeyword(text):
                traffic_num += 1
    return traffic_num,tweet_num

def getQueryStr(t):
    unix_current = time.mktime(time.strptime(t,ISOTIMEFORMAT))    
    unix_tmp = unix_current-3600
    t = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
    q_s = '(.*' + num2month(t[5:7]) + ' ' + t[8:10] + ' ' + t[11:13] +  '.*' + t[0:4] + ')'
    for i in range(1,DELT_T+1):
        unix_tmp = unix_current-i*3600
        t = time.strftime(ISOTIMEFORMAT,time.localtime(unix_tmp))
        q_s = q_s + '|' + '(.*' + num2month(t[5:7]) + ' ' + t[8:10] + ' ' + t[11:13] +  '.*' + t[0:4] + ')'
    return "{'created_at':{'$regex':" + q_s + "}}"

    
def num2month(s):
    if s=='01':
        return 'Jan'
    if s=='02':
        return 'Feb'
    if s=='03':
        return 'Mar'
    if s=='04':
        return 'Apr'
    if s=='05':
        return 'May'
    if s=='06':
        return 'Jun'
    if s=='07':
        return 'Jul'
    if s=='08':
        return 'Aug'
    if s=='09':
        return 'Sep'
    if s=='10':
        return 'Oct'
    if s=='11':
        return 'Nov'
    if s=='12':
        return 'Dec'

def month2num(s):
    if s=='Jan':
        return '01'
    if s=='Feb':
        return '02'
    if s=='Mar':
        return '03'
    if s=='Apr':
        return '04'
    if s=='May':
        return '05'
    if s=='Jun':
        return '06'
    if s=='Jul':
        return '07'
    if s=='Aug':
        return '08'
    if s=='Sep':
        return '09'
    if s=='Oct':
        return '10'
    if s=='Nov':
        return '11'
    if s=='Dec':
        return '12'


def inArea(lat, lon):
    if lat > C_LAT + EDGE or lat < C_ALT - EDGE:
        return False
    if lon > C_LON + EDGE or lon < C_LON - EDGE:
        return False
    return True
       
def hasKeyword(text):
    for word in WORDS:
        if word in text:
            return True
    return False

    

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'usage: python genData_traffic.py decrease/increase high/low result1 result0'
        sys.exit(0)
    T1 = getTime(sys.argv[1])
    T1 = expendTime(T1)
    T0 = getTime(sys.argv[2])
    result1 = []
    result0 = []
    conn = pymongo.Connection(HOST,PORT)
    db = conn[DB_NAME]
    c = db[C_NAME]
    for t in T1:
        traffic_num,tweet_num = tweet_filter(t,c)
        pec = '%.2f' % (float(traffic_num)/float(tweet_num))
        result1.append(t + ' ' + pec + ' ' + traffic_num + ' ' + tweet_num + '\r\n')
    for t in T0:
        traffic_num,tweet_num = tweet_filter(t,c)
        pec = '%.2f' % (float(traffic_num)/float(tweet_num))
        result0.append(t + ' ' + pec + ' ' + traffic_num + ' ' + tweet_num + '\r\n')
    conn.close()
    saveFile(result1, sys.argv[3])
    saveFile(result0, sys.argv[4])


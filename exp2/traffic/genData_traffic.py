# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import time
import datetime

DB_NAME = 'tmp_weibo'
C_NAME = 'beijing'
HOST = '10.214.0.147'
PORT = 27017
ISOTIMEFORMAT='%Y-%m-%dT%XZ'
STEP = 6
DELT_T = 12
EDGE = 0.25
C_LAT = 39.87275
C_LON = 116.3057

POSITIVE_WORDS = [u'堵车',u'塞车',u'堵死了',u'车好多',u'道路拥堵',u'行驶缓慢']
NEGATIVE_WORDS = [u'私信订阅路况，微博应对堵车']

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

def saveFile(lines,file_name):
    f = open(file_name,'w')
    f.writelines(lines)
    f.close()

def tweet_filter(t,c):
    traffic_num = 0
    tweet_num = 0
    start_dt,end_dt = getTimeRange(t)
    records = c.find({'created_at':{'$lt':end_dt,'$gt':start_dt}})
    for r in records:
        text = r['text']
        if inArea(r['lat'],r['lon']):
            tweet_num += 1
            if hasKeyword(text):
                print text
                traffic_num += 1
    return traffic_num,tweet_num

def getTimeRange(t):
    unix_current = time.mktime(time.strptime(t,ISOTIMEFORMAT)) 
    end_dt = datetime.datetime.fromtimestamp(unix_current)
    unix_tmp = unix_current - DELT_T*3600
    start_dt = datetime.datetime.fromtimestamp(unix_tmp)
    return start_dt,end_dt

def inArea(lat, lon):
    if lat > C_LAT + EDGE or lat < C_LAT - EDGE:
        return False
    if lon > C_LON + EDGE or lon < C_LON - EDGE:
        return False
    return True
       
def hasKeyword(text):
    for word in NEGATIVE_WORDS:
        if word in text:
            return False
    for word in POSITIVE_WORDS:
        if word in text:
            return True
    return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python genData_traffic.py station'
        sys.exit(0)
    station = sys.argv[1]
    T1 = getTime('events/'+station+'_increase.txt')
    T1 = expendTime(T1)
    T0 = getTime('events/'+station+'_low.txt')
    result1 = []
    result0 = []
    conn = pymongo.Connection(HOST,PORT)
    db = conn[DB_NAME]
    c = db[C_NAME]
    print 'for increase time stamps'
    for t in T1:
        print t
        traffic_num,tweet_num = tweet_filter(t,c)
        pec = '%.2f' % (float(traffic_num)/float(tweet_num))
        result1.append(t+' '+pec+' '+str(traffic_num)+' '+str(tweet_num)+'\r\n')
    saveFile(result1, 'data_traffic/'+station+'_increase_traffic.txt')
    print 'for low time stamps'
    for t in T0:
        print t
        traffic_num,tweet_num = tweet_filter(t,c)
        pec = '%.2f' % (float(traffic_num)/float(tweet_num))
        result0.append(t+' '+pec+' '+str(traffic_num)+' '+str(tweet_num)+'\r\n')
    saveFile(result0, 'data_traffic/'+station+'_low_traffic.txt')
    conn.close()


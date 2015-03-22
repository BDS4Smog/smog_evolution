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

POSITIVE_WORDS1 = [u'堵车',u'塞车',u'堵死了',u'车好多',u'道路拥堵',u'行驶缓慢',u'好多车']
POSITIVE_WORDS2 = [u'路况好',u'车好少',u'车少',u'交通好',u'路通畅',u'没那么堵',u'不堵车',u'不太堵',u'没堵',u'路况通常',u'交通通畅']
NEGATIVE_WORDS = [u'私信订阅路况，微博应对堵车',u'【北京']

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
    traffic_num1 = 0
    traffic_num2 = 0
    tweet_num = 0
    start_dt,end_dt = getTimeRange(t)
    records = c.find({'created_at':{'$lt':end_dt,'$gt':start_dt}})
    for r in records:
        text = r['text']
        tweet_num += 1
        c = hasKeyword(text)
        if c==1:
            #print text
            traffic_num1 += 1
        if c==2:
            #print text
            traffic_num2 += 1
    return traffic_num1,traffic_num2,tweet_num

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
            return 0
    for word in POSITIVE_WORDS1:
        if word in text:
            return 1
    for word in POSITIVE_WORDS2:
        if word in text:
            return 2
    return False

if __name__ == '__main__':
    #if len(sys.argv) != 2:
    #    print 'usage: python genData_traffic.py station'
    #    sys.exit(0)
    #station = sys.argv[1]
    station = 'beijing'
    T1 = getTime('../events/'+station+'_increase.txt')
    T0 = getTime('../events/'+station+'_low.txt')
    result1 = []
    result0 = []
    conn = pymongo.Connection(HOST,PORT)
    db = conn[DB_NAME]
    c = db[C_NAME]
    
    print 'for increase time stamps'
    for t in T1:
        print t
        traffic_num1,traffic_num2,tweet_num = tweet_filter(t,c)
        if tweet_num != 0:
            pec = '%.5f' % (float(traffic_num1)/float(tweet_num))
        else:
            pec = '0.00000'
        result1.append(t+' '+pec+' '+str(traffic_num1)+" "+str(traffic_num2)+' '+str(tweet_num)+'\r\n')
    saveFile(result1, station+'_raw_increase2.txt')
    
    print 'for low time stamps'
    for t in T0:
        print t
        traffic_num1,traffic_num2,tweet_num = tweet_filter(t,c)
        if tweet_num != 0:
            pec = '%.5f' % (float(traffic_num1)/float(tweet_num))
        else:
            pec = '0.00000'
        result0.append(t+' '+pec+' '+str(traffic_num1)+" "+str(traffic_num2)+' '+str(tweet_num)+'\r\n')
    saveFile(result0, station+'_raw_low2.txt')
    conn.close()


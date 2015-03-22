# -*- coding: utf-8 -*-
import pymongo
import os
import sys
import time
import datetime
import codecs
import jieba

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

#POSITIVE_WORDS = [u'路况',u'拥堵',u'堵',u'堵车',u'塞车',u'堵死了',u'车好多',u'道路拥堵',u'行驶缓慢',u'好多车']
#POSITIVE_WORDS = [u'路况好',u'车好少',u'车少',u'交通好',u'路通畅',u'没那么堵',u'不堵车',u'不太堵',u'没堵',u'路况通常',u'交通通常'u'路堵车']
NEGATIVE_WORDS = [u'【北京市',u'私信订阅路况，微博应对堵车']

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
    conn = pymongo.Connection(HOST,PORT)
    db = conn[DB_NAME]
    c = db[C_NAME]
    
    f = codecs.open('test_data.txt','w','utf-8')
    result=[]


 #   data = c.find({'created_at':{'$lt':end_dt,'$gt':start_dt}})
    data = c.find()
    count = 0
    for d in data:
        
        text = d['text']
        if inArea(d['lat'],d['lon']) and hasKeyword(text):
            timestr = d['created_at'].strftime("%Y-%m-%dT%H:%M:%SZ")
            print timestr
            seg_list = list(jieba.cut(text))
            
            tstr = ""
            for s in seg_list:
                print s.encode('utf-8')
                tstr = tstr+" "+s


            f.write(timestr+'--+--'+tstr+'\r\n')

            count=count+1

    f.close()
    conn.close()


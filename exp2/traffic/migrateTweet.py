import pymongo
import datetime


HOST = '10.214.0.147'
PORT = 27017

DB_NAME = 'CityWeibo_API'
C_NAME = 'beijing'

DB_NAME2 = 'tmp_weibo'
C_NAME2 = 'beijing'

def month2num(s):
    if s=='Jan':
        return 1
    if s=='Feb':
        return 2
    if s=='Mar':
        return 3
    if s=='Apr':
        return 4
    if s=='May':
        return 5
    if s=='Jun':
        return 6
    if s=='Jul':
        return 7
    if s=='Aug':
        return 8
    if s=='Sep':
        return 9
    if s=='Oct':
        return 10
    if s=='Nov':
        return 11
    if s=='Dec':
        return 12

def getTime(c_t):
    year = int(c_t[26:30])
    mon = month2num(c_t[4:7])
    day = int(c_t[8:10])
    hour = int(c_t[11:13])
    minu = int(c_t[14:16])
    sec = int(c_t[17:19])
    return datetime.datetime(year,mon,day,hour,minu,sec)


if __name__ == '__main__':
    conn = pymongo.Connection(HOST,PORT)
    db1 = conn[DB_NAME]
    c1 = db1[C_NAME]
    results = c1.find()
    db2 = conn[DB_NAME2]
    c2 = db2[C_NAME2]
    for i,r in enumerate(results):
        if i%10000 == 0:
            print 'i: ' + str(i)
        if r.has_key('geo')==False or r['geo']==None:
            continue
        if r['geo'].has_key('coordinates')==False or r['geo']['coordinates']==None:
            continue
        if len(r['geo']['coordinates'])!=2:
            continue
        if r.has_key('text') == False:
            continue
        if r.has_key('created_at') == False or r['created_at']==None:
            continue
        text = r['text']
        created_at = r['created_at']
        t = getTime(created_at)
        lat = r['geo']['coordinates'][0]
        lon = r['geo']['coordinates'][1]
        c2.insert({'text':text,'lat':lat,'lon':lon,'created_at':t})
    conn.close()
    





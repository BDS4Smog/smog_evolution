#This program is to call v2 forecast API with a specific (past) time 
#The raw data from API will be stored in mongodb
import pymongo
import datetime 
import sys
import os
import demjson

DB_NAME='forecastio'
HOST='10.214.0.147'
PORT=27017
MY_KEY = '86a5bd6b6fcbd22af6916469cf0433fb'
URL_BASE = 'https://api.forecast.io/forecast/'
TMP_FILE = '/tmp/mydata.json'

def callAPI(my_url):
    os.system('wget ' + my_url + ' -O ' + TMP_FILE)
    f = open(TMP_FILE,'r')
    result=f.readline()
    f.close()
    return result

if __name__ == '__main__':
    if len(sys.argv)!=7:
        sys.stderr.write("usage: python forecastio.py lat lon start_day end_day position city\n")
        sys.exit(1)
    lat =  sys.argv[1]
    lon =  sys.argv[2]
    tmp = sys.argv[3].split('-')
    start_day = datetime.date(int(tmp[0]),int(tmp[1]),int(tmp[2]))
    tmp = sys.argv[4].split('-')
    end_day = datetime.date(int(tmp[0]),int(tmp[1]),int(tmp[2]))
    position_name = sys.argv[5]
    c_name = sys.argv[6]

    print 'Collect data for ' + c_name + ' day by day'

    conn = pymongo.Connection(HOST,PORT)
    db = conn[DB_NAME]
    c = db[c_name]

    day_i = start_day 
    while day_i.isoformat() <= end_day.isoformat():
        my_url = URL_BASE + MY_KEY + '/' + lat + ',' + lon + ',' + day_i.isoformat() + 'T00:00:00' 
        print day_i.isoformat() 
        result = callAPI(my_url)
        result = result[0] + '"position":"' + position_name + '",' + '"date":"' + day_i.isoformat() + '",' + result[1:len(result)]
        text=demjson.decode(result)
        c.insert(text)
        day_i = day_i + datetime.timedelta(1)

    conn.close()

    print 'finished!'




#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import pymongo
import codecs
import time
import datetime
import os

HOST = '10.214.0.144'
PORT = 27017
DB_NAME = 'CityWeibo_API'
C_NAME = 'shanghai_POIs'
C_NAME2 = 'shanghai_checkin'
MAX_RETRY_COUNT = 1200

ACCESS_TOKEN = '2.008x4RGBHfPdrBa6ec7a8c090NwN_q'
URL = 'https://api.weibo.com/2/place/pois/users.json'

log_file = ""

def request_page(poiid,page):
	url = URL
	params = dict(
		access_token=ACCESS_TOKEN,
		poiid=poiid,
		page=page,
		count=50
		)

	try:
		resp = requests.get(url=url, params=params)
	except requests.exceptions.Timeout:
		log("Timeout Error")
		return "[]",-1
	except requests.exceptions.TooManyRedirects:
		log("TooManyRedirects Error")
		return "[]",-1
	except requests.exceptions.RequestException as e:
		log("RequestError:Unknown")
		return "[]",-1


	if resp.text == '{"error":"User requests out of rate limit!","error_code":10023,"request":"/2/place/pois/users.json"}' or resp.text=='{"error":"User requests out of rate limit!","error_code":10023}':
		log("Error:User requests out of rate limit!")
		return resp,-2

	if resp.text =="auth error":
		log("auth error")
		return resp,-1

	if resp.text=="[]" or resp.text=="":
		return "[]",0
	try:
		data = json.loads(resp.text)
	except ValueError:
		log("ValueError")
		return "[]",-1

	if data.has_key('users') and data.has_key('total_number'):
		return data['users'],data['total_number']
	else:
		log("Unknown Error")
		log(resp.text)
		return "[]",0

def get_POIs():
	result=[]
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	c = db[C_NAME]
	pois = c.find()
	for p in pois:
		result.append(p)
	return result


def getTime1(c_t):
	tmp = c_t[26:30]
	year = int(c_t[0:4])
	mon = int(c_t[5:7])
	day = int(c_t[8:10])
	hour = int(c_t[11:13])
	minu = int(c_t[14:16])
	sec = int(c_t[17:19])
	return datetime.datetime(year,mon,day,hour,minu,sec)

def getGender(gender):
	if gender=="m":
		return 1
	elif gender=="f":
		return 0

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

def log(str):
	log_file.write(str+'\r\n')

def getTime2(c_t):
	year = int(c_t[26:30])
	mon = month2num(c_t[4:7])
	day = int(c_t[8:10])
	hour = int(c_t[11:13])
	minu = int(c_t[14:16])
	sec = int(c_t[17:19])
	return datetime.datetime(year,mon,day,hour,minu,sec)

def test():
	request_page('B2094655D06DA5F8409C',1)

def proc_text(data):
	text = {}
	text["user_id"]=data['id']
	text["name"]=data['name']
	text["province"]=data['province']
	text["city"]=data['city']
	text["location"]=data['location']
	text["description"]=data['description']
	text["gender"]=getGender(data['gender'])
	text["created_at"]=getTime2(data['created_at'])
	text["geo_enabled"]=data['geo_enabled']
	text["online_status"]=data['online_status']
	text["checkin_at"]=getTime1(data['checkin_at'])
	return text



def download_chenckin():
	writed_poi = 1
	print 'getting pois'
	pois = get_POIs()
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	collection = db[C_NAME2]

	print 'startting to download data'
	for p in pois:
		
		log("Processing POI: "+p['title'].encode('utf-8'))
		retry_count = 0
		page = 1
		poiid = p['poiid']
		poi_title = p['title']
		poi_lon=p['lon']
		poi_lat=p['lat']
		writed_record=1

		while True:
			
			if retry_count > MAX_RETRY_COUNT:
				break
			data,total = request_page(poiid,page)
			if total==-2:
				time.sleep(1)
			elif total==-1:
				time.sleep(1)
				retry_count+=1
			elif total==0:
				break
			else:
				for i in range(len(data)):
					
					text = proc_text(data[i])
					text['poiid']=poiid
					text['poi_title']=poi_title
					text['poi_lon']=poi_lon
					text['poi_lat']=poi_lat
					log(str(writed_poi)+":"+poi_title.encode('utf-8')+"--"+"total="+str(total)+",writed_record="+str(writed_record))
					collection.insert(text)
					writed_record+=1
				if (total-50*page)<0:
					break
				page+=1
			
		writed_poi+=1
	ofile.close()

if __name__ == "__main__":
	log_file = open('checkin_log.txt','a')
	download_chenckin()
	log_file.close()



'''
def request_total_number(poiid):	
	url = URL
	params = dict(
		access_token=ACCESS_TOKEN,
		poiid=poiid,
		count=50
		)

	resp = requests.get(url=url, params=params)
	
	if resp.text=="[]":
		return 0
	data = json.loads(resp.text)
	if data.has_key('total_number'):
		return data['total_number']
	elif data.has_key('users'):
		return len(data['users'])
	else:
		return 0
	



def download_total_number():
	ofile = codecs.open("totalnumber.txt","w",'utf-8')
	count = 1
	result = []
	pois = get_POIs()
	for p in pois:
		if count>1000:
			break
		total_number = request_total_number(p["poiid"])
		title = p["title"]
#		result.append(str(count)+": "+str(total_number)+" "+title+'\r\n')
		ofile.write(str(count)+": "+str(total_number)+" "+title+'\r\n')
		count+=1
		print count
#	ofile.writelines(result)
	ofile.close()
'''
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
C_NAME2 = 'shanghai_POIs_detail'
MAX_RETRY_COUNT = 1200

ACCESS_TOKEN = '2.008x4RGBHfPdrBa6ec7a8c090NwN_q'
URL = 'https://api.weibo.com/2/place/pois/show.json'

log_file = ""

def request_page(poiid):
	url = URL
	params = dict(
		access_token=ACCESS_TOKEN,
		poiid=poiid,
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

	if resp.text=="[]" or resp.text=="":
		return "[]",0
	try:
		data = json.loads(resp.text)
	except ValueError:
		log("ValueError"+resp.text.encode('utf-8'))
		return "[]",-1

	if data.has_key('poiid'):
		return data,1
	elif data.has_key('error'):
		log("Error: "+data["error"])
		if(data["error"])=="Target poi does not exist!":
			return "[]",0
		return "[]",-1
	else:
		log("Unknown Error")
		log(resp.text.encode('utf-8'))
		return "[]",0

def get_POIs():
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	c = db[C_NAME]
	pois = c.find()
	return pois

def log(text):
	log_file.write(text+'\r\n')


def proc_text(data):
	text = {}
	text["poiid"]=data['poiid']
	text["title"]=data['title']
	text["address"]=data['address']
	text["lon"]=data['lon']
	text["lat"]=data['lat']
	text["category_name"]=data['category_name']
	text["country"]=data['country']
	text["category_id"]=data['categorys']
	text["url"]=data['url']
	text["weibo_id"]=data['weibo_id']
	text["province"]=data['province']
	text["city"]=data['city']
	text["checkin_num"]=data['checkin_num']
	text["postcode"]=data['postcode']
	text["icon"]=data['icon']
	text["checkin_user_num"]=data['checkin_user_num']
	text["tip_num"]=data['tip_num']
	text["photo_num"]=data['photo_num']
	text["todo_num"]=data['todo_num']
	return text

def download_POIs_detail():
	writed_poi = 1
	pois = get_POIs()
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	collection = db[C_NAME2]
	first_record = 2

	for p in pois:
		log("Processing POI: "+p['title'].encode('utf-8'))
		retry_count = 0
		poiid = p['poiid']

		while True:
			if retry_count > MAX_RETRY_COUNT:
				break
			data,total = request_page(poiid)
			if total==-2:
				time.sleep(1)
			if total==-1:
				time.sleep(1)
				retry_count+=1
			elif total==0:
				break
			else:
				text = proc_text(data)
				log(str(writed_poi)+":"+data['title'].encode('utf-8')+" "+data['category_name'].encode('utf-8')+' '+data['categorys'].encode('utf-8'))
				collection.insert(text)
				break
				#log(str(writed_poi)+":"+text['title']+" "+text['category_name']+text['category_id'])
				
			
		writed_poi+=1
	ofile.close()


if __name__ == "__main__":
#	test()
	print "Start"
	log_file = open('POIs_detail_log.txt','a')
	download_POIs_detail()
	log_file.close()
	print "End"
# -*- coding: utf-8 -*-
import json
import requests
import pymongo
import codecs

HOST = '10.214.0.147'
PORT = 27017
DB_NAME = 'CityWeibo_API'
C_NAME = 'beijing_POIs'

ACCESS_TOKEN = '2.008x4RGBHfPdrBa6ec7a8c090NwN_q'
URL = 'https://api.weibo.com/2/place/pois/users.json'

def request_page(poiid,page):
	url = URL
	params = dict(
		access_token=ACCESS_TOKEN,
		poiid=poiid,
		page=page,
		count=50
		)

	resp = requests.get(url=url, params=params)
	
	if resp.text=="[]":
		return "[]",0
	data = json.loads(resp.text)
	print data['total_number']
	return data['users'],len(data['users'])


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
	

def test1():
	users,totalnumber = request_page('B2094654D364ABFB4199',1)
	if totalnumber!=0:
		print "Totalnumber is: "+str(totalnumber)
		for i in range(totalnumber):
			user_id = users[i]['id']
			name = users[i]['name']
			time = users[i]['checkin_at']
			print user_id
			print name.encode('utf-8')
			print time.encode('utf-8')

def get_POIs():
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	c = db[C_NAME]
	pois = c.find()
	return pois

def test2():
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

if __name__ == "__main__":
	test2()
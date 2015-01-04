# -*- coding: utf-8 -*-
import pymongo
import datetime


HOST = '10.214.0.147'
PORT = 27017
DB_NAME = 'CityWeibo_API'
C_NAME_POI = 'beijing_POIs_detail'
C_NAME_CHECKIN = 'beijing_checkin'
STEP = 6
ISOTIMEFORMAT='%Y-%m-%dT%X'

category_list = ["19","44","51","64","115","169","194","258","260","601","500"]

def get_POI_list():
	result = {}
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	c_poi = db[C_NAME_POI]
	data = c_poi.find({},{'poiid':1,'category_id':1})
	for d in data:
		tmp = d['category_id'].split(' ')
		result[d['poiid']] = tmp[0]
	return result

def get_checkin_list():
	result = {}	
	poi_list = get_POI_list()

	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	c_checkin = db[C_NAME_CHECKIN]
	start_time = datetime.datetime(2013,4,20,0,0,0)
	end_time =  datetime.datetime(2014,12,1,0,0,0)
	checkin_list = c_checkin.find({'checkin_at':{'$gt':start_time,'$lt':end_time}},{'poiid':1,'checkin_at':1})
	for c in checkin_list:
		if poi_list.has_key(c['poiid']):
			result[c['checkin_at']] = poi_list[c['poiid']]
	return result

def readtime(filename):
	infile = open(filename,'r')
	data = infile.readlines()
	return data

def get_count(start_time,end_time):
	result={}
	for c in category_list:
		result[c]=0
	for (t,entry) in checkin_list.iteritems():
		if start_time <= t <= end_time:
			if result.has_key(entry)==0:
				log("Error: "+entry+"!!!!!!!!!!!!!")
			else:
				result[entry]+=1
	return result

def process_text(count_list):
	text = ""
	for c in category_list:
		text=text+" "+str(count_list[c])
	return text

def get_checkin_data(ctype):
	result = []
	time_list = readtime('beijing_'+ctype+'.txt')
	an_hour = datetime.timedelta(hours = 1)
	for t in time_list:
		t = t.strip('\r\n')
		log(t)
		#get start and end time
		end_time = datetime.datetime.strptime(t,ISOTIMEFORMAT)
		start_time = end_time-STEP*an_hour
		#count total number
		count_list = get_count(start_time,end_time)
		#save data
		result.append(t+process_text(count_list)+'\r\n')
	ofile = open('beijing_checkin_'+ctype+'.txt','w')
	ofile.writelines(result)
	ofile.close()

def log(string):
	log_file.write(string+'\r\n')

if __name__ == '__main__':
	log_file = open('get_checkin_data.log','a')
	checkin_list = get_checkin_list()
	get_checkin_data('increase')
	get_checkin_data('decrease')
	get_checkin_data('high')
	get_checkin_data('low')
	log_file.close()

	
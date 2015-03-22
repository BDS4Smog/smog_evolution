# -*-coding: utf-8 -*-
import pymongo

ADDRESS = '10.214.0.147'
PORT = 27017
DB_NAME = 'Air'
C_NAME1 = 'Cities'
C_NAME2 = 'Stations'


def complete_shanghai_data():
	result = {}
	conn = pymongo.Connection(ADDRESS,PORT)
	db = conn[DB_NAME]
	collection1 = db[C_NAME1]
	collection2 = db[C_NAME2]

	data = collection2.find({'time_point':{'$gt':'2014-11-30T00:00:00Z','$lt':'2014-12-31T23:59:59Z'},'area':"上海"})
	for d in data:
		t = d['time_point']
		if t[14:16]!="00":
			continue
		if result.has_key(t):
			if d['aqi']!=0:
				result[t]['aqi']+=d['aqi']
				result[t]['aqi_count']+=1
			if d['co']!=0:
				result[t]['co']+=d['co']
				result[t]['co_count']+=1
			if d['so2']!=0:
				result[t]['so2']+=d['so2']
				result[t]['so2_count']+=1
			if d['no2']!=0:
				result[t]['no2']+=d['no2']
				result[t]['no2_count']+=1
			if d['o3']!=0:
				result[t]['o3']+=d['o3']
				result[t]['o3_count']+=1
			if d['pm2_5']!=0:
				result[t]['pm2_5']+=d['pm2_5']
				result[t]['pm2_5_count']+=1
			if d['pm10']!=0:
				result[t]['pm10']+=d['pm10']
				result[t]['pm10_count']+=1

		else:
			t_result = {}
			if d['aqi']!=0:
				t_result['aqi']=d['aqi']
				t_result['aqi_count']=1
			else:
				t_result['aqi']=0
				t_result['aqi_count']=0
			if d['co']!=0:
				t_result['co']=d['co']
				t_result['co_count']=1
			else:
				t_result['co']=0
				t_result['co_count']=0
			if d['so2']!=0:
				t_result['so2']=d['so2']
				t_result['so2_count']=1
			else:
				t_result['so2']=0
				t_result['so2_count']=0
			if d['no2']!=0:
				t_result['no2']=d['no2']
				t_result['no2_count']=1
			else:
				t_result['no2']=0
				t_result['no2_count']=0
			if d['o3']!=0:
				t_result['o3']=d['o3']
				t_result['o3_count']=1
			else:
				t_result['o3']=0
				t_result['o3_count']=0
			if d['pm2_5']!=0:
				t_result['pm2_5']=d['pm2_5']
				t_result['pm2_5_count']=1
			else:
				t_result['pm2_5']=0
				t_result['pm2_5_count']=0
			if d['pm10']!=0:
				t_result['pm10']=d['pm10']
				t_result['pm10_count']=1
			else:
				t_result['pm10']=0
				t_result['pm10_count']=0
			t_result['area']=d['area']
			t_result['time_point']=d['time_point']
			t_result['quality']=""
			result[t]=t_result
	for t in result:
		if result[t]['aqi_count']!=0:
			result[t]['aqi']/=result[t]['aqi_count']
		else:
			result[t]['aqi']=0
		if result[t]['co_count']!=0:
			result[t]['co']/=result[t]['co_count']
		else:
			result[t]['co']=0
		if result[t]['no2_count']!=0:
			result[t]['no2']/=result[t]['no2_count']
		else:
			result[t]['no2']=0
		if result[t]['so2_count']!=0:
			result[t]['so2']/=result[t]['so2_count']
		else:
			result[t]['so2']=0
		if result[t]['o3_count']!=0:
			result[t]['o3']/=result[t]['o3_count']
		else:
			result[t]['o3']=0
		if result[t]['pm2_5_count']!=0:
			result[t]['pm2_5']/=result[t]['pm2_5_count']
		else:
			result[t]['pm2_5']=0
		if result[t]['pm10_count']!=0:
			result[t]['pm10']/=result[t]['pm10_count']
		else:
			result[t]['pm10']=0
		c_aqi = result[t]['aqi']
		if c_aqi<=50:
			result[t]['quality']="优"
		elif c_aqi<=100:
			result[t]['quality']="良"
		elif c_aqi<=150:
			result[t]['quality']="轻度污染"
		elif c_aqi<=200:
			result[t]['quality']="中度污染"
		elif c_aqi<=300:
			result[t]['quality']="重度污染"
		else:
			result[t]['quality']="严重污染"
		del result[t]['aqi_count']
		del result[t]['co_count']
		del result[t]['so2_count']
		del result[t]['no2_count']
		del result[t]['o3_count']
		del result[t]['pm2_5_count']
		del result[t]['pm10_count']

	for t in result:
		collection1.insert(result[t])


if __name__ == '__main__':
	complete_shanghai_data()
#-*- coding: utf-8 -*-
import pymongo

ADDRESS = "10.214.0.147"
PORT = 27017

def select_city():
	conn = pymongo.Connection(ADDRESS,PORT)
	db = conn['Air']
	collection = db['City']
	city_list = collection.find()
	sh_data = collection.find({'area':u'上海'})
	for t in sh_data:
		sh_lat = t['lat']
		sh_lon = t['lon']
	result = {}
	for c in city_list:
		result[c['area']]=(c['lat']-sh_lat)**2+(c['lon']-sh_lon)**2
	sorted_result = sorted(result.iteritems(),key=lambda asd:asd[1])
	for i in sorted_result:
		print i[0].encode('utf-8')
		print i[1]



if __name__ == '__main__':
	select_city()
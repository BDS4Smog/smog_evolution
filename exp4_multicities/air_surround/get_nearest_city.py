#-*- coding: utf-8 -*-
import pymongo
import codecs
ADDRESS = "10.214.0.147"
PORT = 27017

def select_city():
	conn = pymongo.Connection(ADDRESS,PORT)
	db = conn['Air']
	collection = db['City']
	city_list = collection.find()
	sh_data = collection.find({'area':u'北京'})
	for t in sh_data:
		sh_lat = t['lat']
		sh_lon = t['lon']
	result = {}
	for c in city_list:
		result[c['area']]=(c['lat']-sh_lat)**2+(c['lon']-sh_lon)**2
	sorted_result = sorted(result.iteritems(),key=lambda asd:asd[1])
	ofile = open("nearest_city.txt","w")
	for i in sorted_result:
		
		ofile.write("%s %f\r\n"%(i[0].encode("utf8"),i[1]))
	ofile.close()



if __name__ == '__main__':
	select_city()

# -*- coding: utf-8 -*-
import pymongo
import jieba
import datetime

ISOTIMEFORMAT='%Y-%m-%dT%X'
HOST = '10.214.0.147'
PORT = 27017
DB_NAME = 'tmp_weibo'
C_NAME = 'beijing'

KEY_WORDS = ['雾霾','空气质量','雾都','重度污染','蓝天','天好蓝','天很蓝','空气好','污染重','空气差']

def get_selected_data():
	result_text = []
	result_time = []
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	collection = db[C_NAME]

	start_time = datetime.datetime(2013,5,1,0,0,0)
	end_time = datetime.datetime(2014,12,16,0,0,0)
	data = collection.find({'created_at':{'$gt':start_time,'$lt':end_time}},{'text':1,'created_at':1})
	for d in data:
		for k in KEY_WORDS:
			if k in d['text'].encode('utf-8'):
				result_text.append(d['text'].encode('utf-8'))
				result_time.append(d['created_at'])
				break
	return result_text,result_time

def get_all_data():
	result_text = []
	result_time = []
	conn = pymongo.Connection(HOST,PORT)
	db = conn[DB_NAME]
	collection = db[C_NAME]

	data = collection.find({},{'text':1,'created_at':1})
	for d in data:
		result_text.append(d['text'].encode('utf-8'))
		result_time.append(d['created_at'])
	return result_text,result_time

def data_partition(lines):
	result = []
	for l in lines:
		tmp_result = ""
		tmp = l.strip('\r\n').split('我在:http://t.cn')
		tmp = tmp[0].split('我在这里:http://t.cn')
		tmp = tmp[0].split('http://t.cn')
		#print l
		seg_list = jieba.cut(tmp[0])
		#print "---".join(seg_list)
		for s in seg_list:
			tmp_result = tmp_result+s.encode('utf-8')+' '
			#ofile.write(s.encode('utf-8')+' ')
		#ofile.write('\r\n')
		result.append(tmp_result+'\r\n')
	#ofile.close()
	return result

def write_text(result):
	ofile = open('test_selected_text.txt','w')
	ofile.writelines(result)
	ofile.close()

def write_time(result):
	ofile = open('test_selected_time.txt','w')
	for r in result:

		ofile.write(str(r.strftime(ISOTIMEFORMAT))+'\r\n')
	ofile.close()

def log(log_str):
	log_file.write(log_str+'\r\n')

if __name__ == '__main__':
	#log_file = open('OM_log_test.txt','w')
	#get_test_data()
	#log_file.close()
	#data = load_data('Test.txt')
	#data_partition(data)
	print 'downloading data...'
	result_text,result_time = get_selected_data()
	print 'data processing...'
	result_text = data_partition(result_text)
	print 'writing text...'
	write_text(result_text)
	print 'writing time...'
	write_time(result_time)
# -*- coding: utf-8 -*-
import datetime

STEP = 6
ISOTIMEFORMAT='%Y-%m-%dT%X'

def load_time_list(filename):
	infile = open(filename,'r')
	data = infile.readlines()
	infile.close()
	return data

def load_om_data():
	result = {}
	infile = open('test_selected_result.txt','r')
	lines = infile.readlines()
	for l in lines:
		tmp_result = {}
		tmp = l.strip('\r\n').split(' ')
		tmp_result['p1'] = tmp[1]
		tmp_result['p2'] = tmp[2]
		tmp_result['c'] = tmp[3]
		tmp_time = datetime.datetime.strptime(tmp[0],ISOTIMEFORMAT)
		result[tmp_time] = tmp_result
	infile.close()
	return result

def get_count(start_time,end_time):
	result={}
	p1 = 0
	p2 = 0
	c1 = 0
	c2 = 0
	n = 0
	for t in om_data.iterkeys():
		if start_time <= t <= end_time:
			tmp = om_data[t]
			p1=p1+float(tmp['p1'])
			p2=p2+float(tmp['p2'])
			
			if tmp['c']=='1':
				c1+=1
				n = n+1
			elif tmp['c']=='2':
				c2+=1
				n = n+1

	if n!=0:
		p1 = p1/n
		p2 = p2/n
	return p1,p2,c1,c2,n

def gen_om_data(ctype):
	result = []
	time_list = load_time_list('../events/shanghai_'+ctype+'_12h_150.txt')
	an_hour = datetime.timedelta(hours = 1)
	for t in time_list:
		t = t.strip('\r\n')
		#caculate start_time and end_time
		end_time = datetime.datetime.strptime(t,ISOTIMEFORMAT)
		start_time = end_time-STEP*an_hour
		#caculate result
		p1,p2,c1,c2,n= get_count(start_time,end_time)
		#append result
		result.append(t+' '+str(p1)+' '+str(p2)+' '+str(c1)+' '+str(c2)+' '+str(n)+'\r\n')
	#write result
	ofile = open('shanghai_'+ctype+'1.txt','w')
	ofile.writelines(result)
	ofile.close()

if __name__ == '__main__':
	#load om data
	om_data = load_om_data()
	#gen om data
	print 'processing increase...'
	gen_om_data('increase')
	print 'processing decrease...'
	gen_om_data('decrease')
	print 'processing high...'
	gen_om_data('high')
	print 'processing low...'
	gen_om_data('low')
	
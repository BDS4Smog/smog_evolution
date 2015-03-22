# -*- coding: utf-8 -*-
import datetime

STEP = 6
ISOTIMEFORMAT='%Y-%m-%dT%X'

def load_data(filename):
	infile = open(filename,'r')
	data = infile.readlines()
	infile.close()
	return data

def add_total_number(ctype):
	result = []
	#load_om_data
	om_data = load_data('beijing_'+ctype+'1.txt')
	#load_traffic_data
	traffic_data = load_data('../traffic/beijing_'+ctype+'1.txt')
	for o,t in zip(om_data,traffic_data):
		#calculate data
		t = t.strip('\r\n').split(' ')
		t = int(t[5])
		tmp = o.strip('\r\n').split(' ')
		if t!=0:
			positive = float(tmp[3])/t
			negative = float(tmp[4])/t
		else:
			positive = 0
			negative = 0
		#add to result
		result.append(o.strip('\r\n')+' '+str(t)+' '+str(positive)+' '+str(negative)+'\r\n')
	#write data
	ofile = open('beijing_'+ctype+'3.txt','w')
	ofile.writelines(result)
	ofile.close()

if __name__ == '__main__':
	#gen om data
	print 'processing increase...'
	add_total_number('increase')
	print 'processing decrease...'
	add_total_number('decrease')
	print 'processing high...'
	add_total_number('high')
	print 'processing low...'
	add_total_number('low')
	
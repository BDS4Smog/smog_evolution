import datetime
ISOTIMEFORMAT='%Y-%m-%dT%X'

def get_time(ctype):
	result = []
	infile = open('beijing_'+ctype+'_te.txt','r')
	lines = infile.readlines()
	for l in lines:
		result.append(l.strip('\r\n'))
	infile.close()
	return result

def get_record():
	result = {}
	infile = open('beijing_records.txt','r')
	lines = infile.readlines()
	for l in lines:
		tmp = l.strip('\r\n').split(' ')
		result[tmp[0]] = tmp[1]
	infile.close()
	return result

def get_test(ctype):
	result = []
	an_hour = datetime.timedelta(hours = 1)
	time_list = get_time(ctype)
	ofile = open(ctype+'_result.txt','w')
	for t in time_list:
		string = ""
		start_time = datetime.datetime.strptime(t,ISOTIMEFORMAT)
		for i in range(7):
			current = start_time+i*an_hour
			current_time = current.strftime(ISOTIMEFORMAT)
			if result_list.has_key(current_time):
				string = string+result_list[current_time]+"."
			else:
				string = string+"0"+"."
		result.append(string+'\r\n')
	ofile.writelines(result)
	ofile.close()
			



if __name__ == '__main__':
	result_list = get_record()
	print 'increase'
	get_test('increase')
	
	print 'decrease'
	get_test('decrease')
	print 'high'
	get_test('high')
	print 'low'
	get_test('low')
	
	

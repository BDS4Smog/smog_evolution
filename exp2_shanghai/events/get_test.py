FOLDERS1 = ['air','air_surround','mete','mete_surround']
FOLDERS2 = ['traffic_new','opinion_mining','check-in']
#FOLDERS = ['air']

def get_time(ctype):
	result = []
	infile = open('beijing_'+ctype+'_te.txt','r')
	lines = infile.readlines()
	for l in lines:
		result.append(l.strip('\r\n')+'Z')
	infile.close()
	return result


def get_test(ctype):
	time_list = get_time(ctype)
	for f in FOLDERS1:
		te_result = []
		tr_result = []
		infile = open('../'+f+'/beijing_'+ctype+'1.txt','r')
		ofile1 = open('../'+f+'/beijing_'+ctype+'1_tr.txt','w')
		ofile2 = open('../'+f+'/beijing_'+ctype+'1_te.txt','w')
		lines = infile.readlines()
		for i in range(len(lines)):
			flag = 0
			tmp = lines[i].strip('\r\n').split(' ')
			tmp = tmp[0]
			for time in time_list:
				if tmp==time:
					te_result.append(lines[i])
					flag=1
					break
			if flag==0:

				tr_result.append(lines[i])
		ofile1.writelines(tr_result)
		ofile2.writelines(te_result)
		infile.close()
		ofile2.close()
		ofile1.close()

	for f in FOLDERS2:
		te_result = []
		tr_result = []
		infile = open('../'+f+'/beijing_'+ctype+'1.txt','r')
		ofile1 = open('../'+f+'/beijing_'+ctype+'1_tr.txt','w')
		ofile2 = open('../'+f+'/beijing_'+ctype+'1_te.txt','w')
		lines = infile.readlines()
		for i in range(len(lines)):
			flag = 0
			tmp = lines[i].strip('\r\n').split(' ')
			tmp = tmp[0]+'Z'
			for time in time_list:
				if tmp==time:
					te_result.append(lines[i])
					flag=1
					break
			if flag==0:

				tr_result.append(lines[i])
		ofile1.writelines(tr_result)
		ofile2.writelines(te_result)
		infile.close()
		ofile2.close()
		ofile1.close()





if __name__ == '__main__':
	print 'increase'
	get_test('increase')
	
	print 'decrease'
	get_test('decrease')
	print 'high'
	get_test('high')
	print 'low'
	get_test('low')
	
	

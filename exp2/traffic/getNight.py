f = open('haidian_low.txt')
lines = f.readlines()
f.close()
results = []
for line in lines:
    tmp = line.strip().split(' ')
    pec = '%.5f' % (float(tmp[2])/float(tmp[3])*1000)
    hour = int(tmp[0][11:13])
    if hour<=23 and hour>=18: 
        results.append(tmp[0] + ' ' + pec + ' ' + tmp[2] + ' ' + tmp[3] + '\r\n')
f = open('haidian_low_night.txt','w')
f.writelines(results)
f.close()

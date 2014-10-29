f = open('haidian_increase.txt')
lines = f.readlines()
f.close()
results = []
for line in lines:
    tmp = line.strip().split(' ')
    hour = int(line[11:13])
    if hour<=23 and hour>=18: 
        results.append(line)
f = open('haidian_increase_night.txt','w')
f.writelines(results)
f.close()

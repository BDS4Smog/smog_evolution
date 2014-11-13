def readFile(file_name):
    f = open(file_name)
    lines = f.readlines()
    f.close()
    return lines

def writeFile(file_name,lines):
    f = open(file_name,'w')
    f.writelines(lines)
    f.close()

if __name__ == '__main__':
    lines = readFile('beijing_raw_low1.txt')
    results = []
    for line in lines:
        tmp = line.strip().split(' ')
        tweets_num = int(tmp[3])
        hour = int(tmp[0][11:13])
        if tweets_num >= 2000 and hour <= 21 and hour >= 17:
            result = tmp[0] + ' ' + tmp[1] + ' ' + '1' + '\r\n'
            results.append(result)
        else:
            result = tmp[0] + ' ' + tmp[1] + ' ' + '0' + '\r\n'
            results.append(result)
    writeFile('beijing_low1.txt',results)

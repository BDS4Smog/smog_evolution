import sys

def readFile(file_name):
    f = open(file_name)
    lines = f.readlines()
    f.close()
    return lines

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python genData_traffic.py file'
        sys.exit(0)
    lines = readFile(sys.argv[1])
    pec,traf,tweets = 0.0,0,0
    n = 0
    for line in lines:
        tmp = line.strip().split(' ')
        tweets_num = int(tmp[3])
        hour = int(tmp[0][11:13])
        if tweets_num >= 2000 and ((hour >= 17 and hour <= 21) or (hour>=9 and hour<=12)):
#        if tweets_num >= 2000:
            pec += float(tmp[1])
            traf += int(tmp[2])
            tweets +=tweets_num 
            n += 1
    print 'pecentage: %.5f, traffic tweets: %d, tweets: %d' % (pec/n, traf/n, tweets/n)

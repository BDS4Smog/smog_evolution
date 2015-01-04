import matplotlib.pyplot as plt 
import numpy as np 

SmogOpin = 2
Traffics = 2
POIs = 11
def checkInData(fileName):
    f = open(fileName)
    lines = f.readlines()
    data = np.zeros([len(lines),POIs]) 
    for i,line in enumerate(lines):
        tmp = line.strip().split(' ')
        for j in range(POIs):
            data[i][j] = int(tmp[j+1])
    f.close()
    return data

def calCheckinAvg(d):
    avg = []
    avg.append(np.average(d[:,3]))
    avg.append(np.average(d[:,5]))
    avg.append(np.average(d[:,4]))
    avg.append(np.average(d[:,0]))
    avg.append(np.average(d[:,6]))
    avg.append(np.average(d[:,7]))
    avg.append(np.average(d[:,1]))
    avg.append(np.average(d[:,2]))
    avg.append(np.average(d[:,9]))
    avg.append(np.average(d[:,10]))
    return np.array(avg)

def getCheckinName():
    name = ['Restaurant','Entetainment','Shop','Hotel','Outdoor&Park','Company','Office&Buiding','Campus','Site','Others']
    return np.array(name) 

def calCheckinPec(file1,file2):
    checkin_d1 = checkInData(file1)
    checkin_d2 = checkInData(file2)
    avg1 = calCheckinAvg(checkin_d1)
    avg2 = calCheckinAvg(checkin_d2)
#    avg1[1] += 2
#    avg1[2] += 1 
#    avg2[3] -= 6 
#    avg2[6] += 2
#    avg2[7] += 2
    print avg1
    print avg2
    return avg1,avg2

def smogOpinionData(fileName):
    f = open(fileName)
    lines = f.readlines()
    data = np.zeros([len(lines),2]) 
    for i,line in enumerate(lines):
        tmp = line.strip().split(' ')
        data[i][0] = float(tmp[7])
        data[i][1] = float(tmp[8])
    f.close()
    return data

def trafficData(fileName):
    f = open(fileName)
    lines = f.readlines()
    data = []
    for i,line in enumerate(lines):
        tmp = line.strip().split(' ')
        if int(tmp[5])>2000:
            data.append([float(tmp[1]),float(tmp[2])])
    f.close()
    return np.array(data)

def trafficData2(fileName):
    f = open(fileName)
    lines = f.readlines()
    data = []
    for i,line in enumerate(lines):
        tmp = line.strip().split(' ')
        hour = int(tmp[0][11:13])
        if int(tmp[5])>2000 and hour<=21 and hour>=17:
            data.append([float(tmp[1]),float(tmp[2])])
    f.close()
    return np.array(data)

def calSmogOpinionPec(file1,file2):
    d1 = smogOpinionData(file1)
    d2 = smogOpinionData(file2)
    avg1 = []
    avg2 = []
    avg1.append(np.average(d1[:,0]))
    avg1.append(np.average(d1[:,1]))
    avg2.append(np.average(d2[:,0]))
    avg2.append(np.average(d2[:,1]))
    return np.array(avg1),np.array(avg2)

def calTrafficPec(file1,file2):
    d1 = trafficData(file1)
    d2 = trafficData(file2)
    d12 = trafficData2(file1)
    d22 = trafficData2(file2)

    avg1 = []
    avg1.append(np.average(d1[:,0]))
    avg1.append(np.average(d12[:,0]))

    avg2 = []
    avg2.append(np.average(d2[:,0]))
    avg2.append(np.average(d22[:,0]))
    return np.array(avg1),np.array(avg2)

def autolabel(rects):
    for i,rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%.1f'%float(height),ha='center', va='bottom',fontsize=15)

def autolabel2(rects):
    for i,rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%.3f%%'%float(height),ha='center', va='bottom',fontsize=15)

def autoPec(rects1,rects2,p):
    for i, rect1 in enumerate(rects1):
        rect2 = rects2[i]
        height1 = rect1.get_height()
        height2 = rect2.get_height()
        height = height1
        pec = (height1 - height2)/height2
        label = '+'
        if height1 < height2: 
            height = height2
            pec = (height2 - height1)/height1
            label = '-'
        plt.text(rect1.get_x()+rect1.get_width()/2., height*p, label+'%.1f%%'%(pec*100), va='top',color='b',fontsize=16)

def autoPec2(rects1,rects2,p):
    for i, rect1 in enumerate(rects1):
        rect2 = rects2[i]
        height1 = rect1.get_height()
        height2 = rect2.get_height()
        height = height1
        pec = (height1 - height2)/height2
        label = '+'
        if height1 < height2: 
            height = height2
            pec = (height2 - height1)/height1
            label = '-'
        plt.text(rect1.get_x()+rect1.get_width()/2., height+p, label+'%.1f%%'%(pec*100), va='top',color='b',fontsize=16)

if __name__ == '__main__':
    y1,y2 = calCheckinPec('../check-in/beijing_increase1.txt','../check-in/beijing_low1.txt')
    name_all = getCheckinName()
    width = 0.45
    font = {'size':16.5}
    plt.rc('font',**font)
    plt.subplot2grid((2,4),(0,0))
    x=np.array([0])
    y=np.array([y1[2]])
    yy=np.array([y2[2]])
    name=np.array([name_all[2]])
    rects1 = plt.bar(x,y,width,color='r',align='center')
    rects2 = plt.bar(x+width,yy,width,color='y',align='center')
    plt.xlim([-0.5,1])
    plt.xticks(x+width/2,name,rotation=0)
    plt.ylim([0,9])
    plt.ylabel('Avg Checkin #')
    plt.legend(['A','N-A'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    autolabel(rects1)
    autolabel(rects2)
    autoPec(rects1,rects2,1.34)

    plt.subplot2grid((2,4),(0,1))
    x=np.array([0])
    y=np.array([y1[4]])
    yy=np.array([y2[4]])
    name=np.array([name_all[4]])
    rects1 = plt.bar(x,y,width,color='r',align='center')
    rects2 = plt.bar(x+width,yy,width,color='y',align='center')
    plt.xlim([-0.5,1])
    plt.xticks(x+width/2,name,rotation=0)
    plt.ylim([0,90])
    autolabel(rects1)
    autolabel(rects2)
    autoPec(rects1,rects2,1.3)

    plt.subplot2grid((2,4),(0,2))
    x=np.array([0])
    y=np.array([y1[6]])
    yy=np.array([y2[6]])
    name=np.array([name_all[6]])
    rects1 = plt.bar(x,y,width,color='r',align='center')
    rects2 = plt.bar(x+width,yy,width,color='y',align='center')
    plt.xlim([-0.5,1])
    plt.xticks(x+width/2,name,rotation=0)
    plt.ylim([0,50])
    autolabel(rects1)
    autolabel(rects2)
    autoPec(rects1,rects2,1.3)

    plt.subplot2grid((2,4),(0,3))
    x=np.array([0])
    y=np.array([y1[7]])
    yy=np.array([y2[7]])
    name=np.array([name_all[7]])
    rects1 = plt.bar(x,y,width,color='r',align='center')
    rects2 = plt.bar(x+width,yy,width,color='y',align='center')
    plt.xlim([-0.5,1])
    plt.xticks(x+width/2,name,rotation=0)
    plt.ylim([0,35])
    autolabel(rects1)
    autolabel(rects2)
    autoPec(rects1,rects2,1.32)


    y1,y2 = calTrafficPec('../traffic/beijing_increase2.txt','../traffic/beijing_low2.txt')
    y1 = y1*100
    y2 = y2*100
    plt.subplot2grid((2,4),(1,0),colspan=2)
    x=np.array([0,1])
    name=np.array(['Traffic jam tweet\n(Hour: 00-24)','Traffic jam tweet\n(Hour: 17-21)'])
    rects1 = plt.bar(x,y1,width,color='r',align='center')
    rects2 = plt.bar(x+width,y2,width,color='y',align='center')
    plt.xlim([-0.5,2])
    plt.xticks(x+width/2,name,rotation=0)
    plt.ylim([0,0.4])
    plt.ylabel('Tweet percentage %')
    autolabel2(rects1)
    autolabel2(rects2)
    autoPec2(rects1,rects2,0.07)


    y1,y2 = calSmogOpinionPec('../opinion_mining/beijing_increase1.txt','../opinion_mining/beijing_low1.txt')
#    y1=np.array([0.00101,0.00081])
#    y2=np.array([0.00061,0.00091])
    print y1
    print y2
    y1 = y1*100
    y2 = y2*100
    plt.subplot2grid((2,4),(1,2),colspan=2)
    x=np.array([0,1])
    name=np.array(['Smog disaster tweet','Good air tweet'])
    rects1 = plt.bar(x,y1,width,color='r',align='center')
    rects2 = plt.bar(x+width,y2,width,color='y',align='center')
    plt.xlim([-0.5,2])
    plt.xticks(x+width/2,name,rotation=0)
    plt.ylim([0,0.16])
    autolabel2(rects1)
    autolabel2(rects2)
    autoPec2(rects1,rects2,0.03)

    plt.show()


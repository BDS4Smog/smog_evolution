import matplotlib.pyplot as plt 
import numpy as np 

def autolabel(rects):
    for i,rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%.1f%%'%float(height),ha='center', va='bottom',fontsize=11.5)

if __name__ == '__main__':
    width = 0.35

    font = {'size':17.5}
    plt.rc('font',**font)

    plt.subplot2grid((1,3),(0,0))
    y1 = np.array([2.93,1.06])
    y2 = np.array([3.17,0.71])
    y3 = np.array([3.99,1.88])
    x=np.array([0,1.45])
    name=np.array(['Appearance','Disappearance'])
    rects1 = plt.bar(x,y1,width,color='r',align='center')
    rects2 = plt.bar(x+width,y2,width,color='y',align='center')
    rects3 = plt.bar(x+2*width,y3,width,color='b',align='center')
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    plt.xlim([-0.5,2.7])
    plt.ylim([0,4.3])
    plt.ylabel('Improvement %')
    plt.xticks(x+width,name,rotation=0)
    plt.title('Precision')
    plt.legend(['$F_s^m$','$F_s^t$','$F_s^o$'],loc=1)

    plt.subplot2grid((1,3),(0,1))
    y1 = np.array([0.77,1.91])
    y2 = np.array([2.41,3.03])
    y3 = np.array([2.63,3.14])
    x=np.array([0,1.45])
    name=np.array(['Appearance','Disappearance'])
    rects1 = plt.bar(x,y1,width,color='r',align='center')
    rects2 = plt.bar(x+width,y2,width,color='y',align='center')
    rects3 = plt.bar(x+2*width,y3,width,color='b',align='center')
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    plt.xlim([-0.5,2.7])
    plt.ylim([0,4.3])
    plt.xticks(x+width,name,rotation=0)
    plt.title('Recall')

    plt.subplot2grid((1,3),(0,2))
    y1 = np.array([1.93,1.73])
    y2 = np.array([2.72,2.19])
    y3 = np.array([3.29,2.65])
    x=np.array([0,1.45])
    name=np.array(['Appearance','Disappearance'])
    rects1 = plt.bar(x,y1,width,color='r',align='center')
    rects2 = plt.bar(x+width,y2,width,color='y',align='center')
    rects3 = plt.bar(x+2*width,y3,width,color='b',align='center')
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    plt.xlim([-0.5,2.7])
    plt.ylim([0,4.3])
    plt.xticks(x+width,name,rotation=0)
    plt.title('F1 Score')

    plt.show()

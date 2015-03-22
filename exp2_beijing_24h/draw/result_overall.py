import matplotlib.pyplot as plt 
import numpy as np 

def autolabel(rects):
    for i,rect in enumerate(rects):
        width = rect.get_width()
        height = rect.get_height()
        plt.text(1.02*width,rect.get_y()+height/2., '%.1f%%'%float(width),fontsize=17)

if __name__ == '__main__':
    width = 0.13

    font = {'size':18}
    plt.rc('font',**font)

    x1 = np.array([89.1,87.6])
    x2 = np.array([85.4,84.7])
    y=np.array([0,0.35])
    name=np.array(['Beijing','Shanghai'])
    rects1 = plt.barh(y,x1,width,color='r',align='center')
    rects2 = plt.barh(y+width,x2,width,color='b',align='center')
    autolabel(rects1)
    autolabel(rects2)
    plt.xlim([0,100])
    plt.ylim([-0.1,0.7])
    plt.xlabel('Accuracy %')
    plt.yticks(y+width/2,name,rotation=-90)
    plt.legend(['Web Science Approach','China Meteorological Agency'],loc=1, ncol=2,fontsize=15)

    plt.show()

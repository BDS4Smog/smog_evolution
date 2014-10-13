'''
Calculate Markov Matrix
'''
import numpy as np
import sys

LABEL_NUM = 6
SPAN_NUM = 4

def readFile(file_name):
    f = open(file_name,'r')
    lines = f.readlines()
    f.close()
    return lines
   
def loadTranMap(file_name):
    lines = readFile(file_name)
    T = np.zeros((SPAN_NUM,LABEL_NUM,LABEL_NUM))
    for line in lines:
        arr = line.strip().split(' ')
        k = int(arr[2]) - 1
        s1 = int(arr[4]) - 1
        s2 = int(arr[6]) - 1
        T[k][s1][s2] = T[k][s1][s2] + 1
    return T


def statisticsTran(T):
    M = np.zeros((SPAN_NUM,LABEL_NUM,LABEL_NUM))
    for k in range(0,SPAN_NUM):
        for i in range(0,LABEL_NUM):
            n = 0
            for j in range(0,LABEL_NUM):
                n = n + T[k][i][j]
            for j in range(0,LABEL_NUM):
                M[k][i][j] = float(T[k][i][j])/float(n)
    return M 
        

def calM(sample_file):
    T = loadTranMap(sample_file)    
    M = statisticsTran(T) 
    return M 



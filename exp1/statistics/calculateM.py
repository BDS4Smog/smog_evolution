'''
Calculate Markov Matrix
'''
import numpy as np
import sys

LABEL_NUM = 6

def readFile(file_name):
    f = open(file_name,'r')
    lines = f.readlines()
    f.close()
    return lines
   
def loadTranMap(file_name):
    lines = readFile(file_name)
    T = np.zeros((LABEL_NUM,LABEL_NUM))
    for line in lines:
        arr = line.strip().split(' ')
        s1 = int(arr[3]) - 1
        s2 = int(arr[5]) - 1
        T[s1][s2] = T[s1][s2] + 1
    return T


def statisticsTran(T):
    t = np.zeros((LABEL_NUM,LABEL_NUM))
    for i in range(0,LABEL_NUM):
        n = 0
        for j in range(0,LABEL_NUM):
            n = n + T[i][j]
        for j in range(0,LABEL_NUM):
            t[i][j] = float(T[i][j])/float(n)
    return t
        

def calM(sample_file):
    T = loadTranMap(sample_file)    
    M = statisticsTran(T) 
    return M 



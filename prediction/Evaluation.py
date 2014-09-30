DIR='../statistics/'
import sys
import numpy as np
sys.path.append(DIR)
import calculateM as cm

def print_status(S):
    my_str = '('
    for i in range(0,S.shape[1]-1):
        my_str = my_str + str(S[0][i]) + ','
    my_str = my_str + str(S[0][S.shape[1]-1]) + ')'
    print my_str

def Markov_process(M,V,K):
    for i in range(0,K):
        V = np.dot(V,M)
    return V

if __name__ == '__main__':
    M = cm.calM(DIR + 'station_Changping.txt')

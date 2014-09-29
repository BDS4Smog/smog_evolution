'''
Input: Markov matrix M, current status vector V, parameter K
Output: status vectors in the future K hours
'''

import numpy as np
import sys

def status_print(S):
    my_str = '('
    for i in range(0,S.shape[1]-1):
        my_str = my_str + str(S[0][i]) + ','
    my_str = my_str + str(S[0][S.shape[1]-1]) + ')'
    print my_str

if __name__ == '__main__':
    m_f = sys.argv[1]
    v_f = sys.argv[2]
    K = int(sys.argv[3])
    M=np.load(m_f)
    V=np.load(v_f)
    for i in range(0,K):
        V = np.dot(V,M)
        status_print(V)
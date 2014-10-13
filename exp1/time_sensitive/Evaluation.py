import sys
import numpy as np
import calculateM as cm

def print_vector(V):
    my_str = '('
    for i in range(0,V.shape[0]-1):
        my_str = my_str + str(V[i]) + ','
    my_str = my_str + str(V[V.shape[0]-1]) + ')'
    print my_str

def Markov_process(M,p,K):
    V = labelToVector(p)
    for i in range(0,K):
        V = np.dot(V,M)
    l = vectorToLabel(V)
    return l 

def labelToVector(l):
    V=np.zeros(cm.LABEL_NUM)
    V[l-1]=1
    return V

def vectorToLabel(V):
    val = V.max()
    for i in range(0,V.shape[0]-1):
        if V[i] == val:
            return i+1 

def loadTest(test_file):
    lines = cm.readFile(test_file)
    Ps={}
    Ts={}
    for k in range(0,cm.SPAN_NUM):
        Ps[k]=[]
        Ts[k]=[]
    for line in lines:
        tmp = line.strip().split(' ')
        k = int(tmp[2]) - 1
        Ps[k].append(int(tmp[4])-1)
        Ts[k].append(int(tmp[6])-1)
    return Ps,Ts

def predict(M,P,K):
    PP=[]
    for p in P:
        l = Markov_process(M,p,K)
        PP.append(l)
    return PP

def calAcc(PP,T):
    num = 0
    size = len(PP)
    for i in range(0,size):
        if PP[i]==T[i]:
            num = num + 1
    return float(num)/float(size)

if __name__ == '__main__':
    if len(sys.argv)!=4:
       sys.stderr.write("usage: python Evaluation.py train_file test_file K\n")
       sys.exit(1)
    train_file = sys.argv[1]
    M = cm.calM(train_file)
    K = int(sys.argv[3])
    test_file = sys.argv[2]
    Ps,Ts=loadTest(test_file)
    for k in range(0,cm.SPAN_NUM):
        PP=predict(M[k],Ps[k],K)
        acc = calAcc(PP,Ts[k])
        print 'Span:' + str(k+1) +  ', accuracy: ' + str(acc)


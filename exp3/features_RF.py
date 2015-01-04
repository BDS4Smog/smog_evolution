import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
import pylab as pl
import sys 
import random

VERSION = 1
LIMIT_OF_EMPTY = 3

def readData(View,Station,Type):
    Atts = []
    Labs = []
    fileName0 = ''
    fileName1 = ''
    if Type=='increase':
        fileName0 = View + '/' + Station + '_low' + str(VERSION) + '.txt'  
        fileName1 = View + '/' + Station + '_increase' + str(VERSION) + '.txt'  
    else:
        fileName0 = View + '/' + Station + '_low' + str(VERSION) + '.txt'  
        fileName1 = View + '/' + Station + '_increase' + str(VERSION) + '.txt'  

    f = open(fileName1)
    lines = f.readlines()
    for line in lines:
        tmp = line.strip().split(' ')
        xs = []
        for x in tmp[1:]:
            xs.append(float(x))
        if xs.count(-1) <= LIMIT_OF_EMPTY:
            Atts.append(xs)
            Labs.append(1.0)

    num = len(Atts)
    
    f = open(fileName0)
    lines = f.readlines()
    random.shuffle(lines)
    for line in lines:
        tmp = line.strip().split(' ')
        xs = []
        for i in range(1,len(tmp)):
            xs.append(float(tmp[i]))
        if xs.count(-1) <= LIMIT_OF_EMPTY:
            Atts.append(xs)
            Labs.append(0.0)
        if len(Atts) == 2*num:
            break

    return np.array(Atts),np.array(Labs)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write("usage: python features_RF.py View Station Type\n")
        sys.exit(1)
    View = sys.argv[1]
    Station = sys.argv[2]
    Type = sys.argv[3]
    X,y = readData(View,Station,Type)
    forest = ExtraTreesClassifier(n_estimators=250,random_state=0)
    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
    indices = np.argsort(importances)[::-1]

    X_num = X.shape[1]
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(0,X_num):
        print("%d. feature %d (%f) (%f)" % (f + 1, indices[f], importances[indices[f]],std[indices[f]]))

    # Plot the feature importances of the forest
    pl.figure()
    pl.title("Feature Importance")
    pl.bar(range(X_num), importances[indices], color="r", yerr=std[indices], align="center")
    pl.xticks(range(10), indices)
    pl.xlim([-1, X_num])
    pl.show()

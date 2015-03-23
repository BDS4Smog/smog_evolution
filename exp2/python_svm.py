import numpy
from sklearn import svm
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.multiclass import OneVsRestClassifier

if __name__ == "__main__":
    print "start"
    tr = numpy.loadtxt("./trdata_for_python.txt")
    te = numpy.loadtxt("./tedata_for_python.txt")

    #SVM
    #clf = svm.SVC(C=1.0,kernel='linear',probability=True)
    #clf.fit(tr[:,1:-1],tr[:,0])
    #y = clf.predict_proba(te[:,1:-1])

    #logistic regression
    clf = linear_model.LogisticRegression(penalty="l2",dual=True)
    clf.fit(tr[:,1:-1],tr[:,0])
    y = clf.predict_proba(te[:,1:-1])
    #clf = KNeighborsClassifier(n_neighbors=2)

    #classifier = OneVsRestClassifier(clf)
    #y_score = classifier.fit(tr[:,1:-1],tr[:,0]).decision_function(te[:,1:-1])

    fpr, tpr, thresholds = metrics.roc_curve(te[:,0], y[:,1])
    auc = metrics.auc(fpr, tpr)
    print 'AUC: '
    print auc


    print "end" 
    

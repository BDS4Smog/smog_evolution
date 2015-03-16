import matplotlib.pyplot as plt 
import numpy as np 

if __name__ == '__main__':
    x = np.array([2,3,4,5,6,7])
    a_melm=np.array([[0.812,0.847,0.852,0.877,0.880,0.914],[0.840,0.902,0.913,0.920,0.947,0.954],[0.825,0.873,0.881,0.898,0.912,0.934]])
    e_melm=np.array([[0.740,0.822,0.850,0.859,0.890,0.888],[0.746,0.858,0.891,0.908,0.923,0.935],[0.742,0.838,0.867,0.882,0.906,0.909]])
    a_elm=np.array([[0.794,0.825,0.823,0.811,0.812,0.828],[0.830,0.861,0.892,0.901,0.898,0.905],[0.812,0.842,0.856,0.853,0.852,0.864]])
    e_elm=np.array([[0.725,0.762,0.793,0.808,0.804,0.811],[0.727,0.779,0.797,0.841,0.818,0.849],[0.725,0.770,0.793,0.823,0.810,0.829]])
    a_bp=np.array([[0.777,0.788,0.845,0.837,0.853,0.869],[0.802,0.853,0.919,0.877,0.904,0.928],[0.788,0.819,0.880,0.856,0.877,0.896]])
    e_bp=np.array([[0.707,0.773,0.854,0.858,0.827,0.846],[0.745,0.798,0.859,0.881,0.887,0.891],[0.725,0.785,0.856,0.869,0.855,0.868]])
    a_rf=np.array([[0.818,0.849,0.860,0.867,0.899,0.910],[0.848,0.873,0.883,0.897,0.899,0.901],[0.832,0.860,0.871,0.880,0.899,0.905]])
    e_rf=np.array([[0.723,0.758,0.859,0.846,0.869,0.901],[0.806,0.836,0.867,0.874,0.873,0.865],[0.762,0.794,0.861,0.859,0.870,0.882]])

    params = {'legend.fontsize': 9,
              'legend.linewidth': 1}
    plt.rcParams.update(params)
    plt.subplot2grid((3,2),(0,0))
    plt.plot(x,a_melm[0],'r*-')
    plt.plot(x,a_elm[0],'go-')
    plt.plot(x,a_bp[0],'k^-')
    plt.plot(x,a_rf[0],'b+-')
    plt.xlim([1.5,7.5])
    plt.ylim([0.76,0.95])
    plt.ylabel('Precision')
    plt.title('Smog disaster appearance')
    plt.legend(['M-ANN','ELM','BP', 'RF'],loc=2)

    plt.subplot2grid((3,2),(0,1))
    plt.plot(x,e_melm[0],'r*-')
    plt.plot(x,e_elm[0],'go-')
    plt.plot(x,e_bp[0],'k^-')
    plt.plot(x,e_rf[0],'b+-')
    plt.xlim([1.5,7.5])
    plt.title('Smog disaster disappearance')

    plt.subplot2grid((3,2),(1,0))
    plt.plot(x,a_melm[1],'r*-')
    plt.plot(x,a_elm[1],'go-')
    plt.plot(x,a_bp[1],'k^-')
    plt.plot(x,a_rf[1],'b+-')
    plt.xlim([1.5,7.5])
    plt.ylabel('Recall')

    plt.subplot2grid((3,2),(1,1))
    plt.plot(x,e_melm[1],'r*-')
    plt.plot(x,e_elm[1],'go-')
    plt.plot(x,e_bp[1],'k^-')
    plt.plot(x,e_rf[1],'b+-')
    plt.xlim([1.5,7.5])

    plt.subplot2grid((3,2),(2,0))
    plt.plot(x,a_melm[2],'r*-')
    plt.plot(x,a_elm[2],'go-')
    plt.plot(x,a_bp[2],'k^-')
    plt.plot(x,a_rf[2],'b+-')
    plt.xlim([1.5,7.5])
    plt.xlabel('# of views (n)')
    plt.ylabel('F1 Score')

    plt.subplot2grid((3,2),(2,1))
    plt.plot(x,e_melm[2],'r*-')
    plt.plot(x,e_elm[2],'go-')
    plt.plot(x,e_bp[2],'k^-')
    plt.plot(x,e_rf[2],'b+-')
    plt.xlim([1.5,7.5])
    plt.xlabel('# of views (n)')

    plt.show()

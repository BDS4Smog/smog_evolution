import matplotlib.pyplot as plt 
import numpy as np 

if __name__ == '__main__':
    x = np.array([2,3,4,5,6])
    a_melm=np.array([[0.8499,0.8871,0.9126,0.9398,0.9610],[0.8116,0.8452,0.8565,0.8820,0.8856],[0.8293,0.8632,0.8835,0.9094,0.9221]])
    e_melm=np.array([[0.7462,0.8474,0.8763,0.8951,0.9124],[0.7295,0.8055,0.8144,0.8480,0.8556],[0.7366,0.8256,0.8425,0.8705,0.8825]])
    a_elm=np.array([[0.8193,0.8833,0.8910,0.8838,0.8910],[0.7983,0.8045,0.8187,0.8126,0.8264],[0.8075,0.8408,0.8522,0.8455,0.8564]])
    e_elm=np.array([[0.741,0.806,0.797,0.808,0.807],[0.737,0.791,0.771,0.775,0.781],[0.738,0.797,0.783,0.790,0.793]])
    a_rf=np.array([[0.8575,0.8682,0.9018,0.9099,0.9117],[0.8463,0.8689,0.8628,0.8869,0.9118],[0.8507,0.8677,0.8812,0.8977,0.911]])
    e_rf=np.array([[0.7788,0.8097,0.8172,0.8471,0.8528],[0.7808,0.8013,0.7938,0.8663,0.8745],[0.7785,0.8039,0.8044,0.8554,0.8627]])

    params = {'legend.fontsize': 9,
              'legend.linewidth': 1}
    plt.rcParams.update(params)
    plt.subplot2grid((3,2),(0,0))
    plt.plot(x,a_melm[0],'r*-')
    plt.plot(x,a_elm[0],'go-')
    plt.plot(x,a_rf[0],'b+-')
    plt.xlim([1,7])
    plt.ylabel('Precision')
    plt.title('Smog disaster appearance')
    plt.legend(['Multi-ELM','ELM','RF'],loc=2)

    plt.subplot2grid((3,2),(0,1))
    plt.plot(x,e_melm[0],'r*-')
    plt.plot(x,e_elm[0],'go-')
    plt.plot(x,e_rf[0],'b+-')
    plt.xlim([1,7])
    plt.title('Smog disaster elimination')

    plt.subplot2grid((3,2),(1,0))
    plt.plot(x,a_melm[1],'r*-')
    plt.plot(x,a_elm[1],'go-')
    plt.plot(x,a_rf[1],'b+-')
    plt.xlim([1,7])
    plt.ylabel('Recall')

    plt.subplot2grid((3,2),(1,1))
    plt.plot(x,e_melm[1],'r*-')
    plt.plot(x,e_elm[1],'go-')
    plt.plot(x,e_rf[1],'b+-')
    plt.xlim([1,7])

    plt.subplot2grid((3,2),(2,0))
    plt.plot(x,a_melm[2],'r*-')
    plt.plot(x,a_elm[2],'go-')
    plt.plot(x,a_rf[2],'b+-')
    plt.xlim([1,7])
    plt.xlabel('# of views (n)')
    plt.ylabel('F1 Score')

    plt.subplot2grid((3,2),(2,1))
    plt.plot(x,e_melm[2],'r*-')
    plt.plot(x,e_elm[2],'go-')
    plt.plot(x,e_rf[2],'b+-')
    plt.xlim([1,7])
    plt.xlabel('# of views (n)')

    plt.show()

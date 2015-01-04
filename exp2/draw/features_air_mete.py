from pylab import * 

importances1 = [0.3106,0.173,0.1638,0.159,0.1031,0.0904]
std1 = [0.123,0.0897,0.0573,0.084,0.0378,0.0183]
len1 = len(importances1)
x1 = range(len1)
indices1 = ['PM2.5','PM10','SO2','CO','NO2','O3'] 

importances2 = [0.2132,0.1864,0.1611,0.1587,0.128,0.0979,0.0546]
std2 = [0.027,0.0241,0.0233,0.0222,0.0213,0.0187,0.0133]
len2 = len(importances2)
x2 = range(len2)
indices2 = ['wind_direction','temperature','humidity','pressure','wind_speed','clouds','rain_in_3h']

font = {'size':15}
rc('font',**font)

subplot(1,2,1)
bar(x1, importances1,color="r", yerr=std1, align="center")
rc('xtick', labelsize=12) 
#rc('ytick', labelsize=12) 
title('Air Pollutants')
xticks(x1, indices1)
xlim([-1, len1])
ylabel('Importance')

subplot(1,2,2)
bar(x2, importances2, color="r", yerr=std2, align="center")
#rc('xtick', labelsize=4) 
#rc('ytick', labelsize=8) 
title('Meteorological Conditions')
ylabel('Importance')
xticks(x2, indices2,rotation=16)
xlim([-1, len2])

show()



# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 15:35:00 2017
compare  isothermal layer depth(ILD) of 2 turtle data and 3 model data.
@author: yifan
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import  timedelta
from turtleModule import  str2ndlist, np_datetime
import utilities

example=[117170,129775,118905,129779] # those turtle's id is random  
T=[]  # get all information of four example turtle
for e in range(len(example)):
    obsData = pd.read_csv('ctdWithModTempByDepth.csv')
    obs_data=pd.read_csv('ctd_good_new.csv')
    tf_index = np.where(obsData['TF'].notnull())[0]
    obsturtle_id=pd.Series(obsData['PTT'][tf_index],index=tf_index)
    indx=[]  
    for i in tf_index:
        if obsturtle_id[i]==example[e]:   # we can get each turtle's ILD
            indx.append(i)
    Temp = pd.Series(str2ndlist(obsData['TEMP_VALS'][indx]), index=indx)
    Indx=[] # get rid of the profile without ten record points
    for i in indx:
        if len(Temp[i])==10:
            Indx.append(i)
    Data = obsData.ix[Indx]
    obs_data=obs_data.ix[Indx]                    
    obsTime = pd.Series(np_datetime(Data['END_DATE'].values), index=Indx)
    obsTemp = pd.Series(str2ndlist(Data['TEMP_VALS'].values), index=Indx)
    obsDepth = pd.Series(str2ndlist(Data['TEMP_DBAR'].values), index=Indx)
    modDepth = pd.Series(str2ndlist(obs_data['LayerDepth'], bracket=True), index=Indx) # If str has '[' and ']', bracket should be True.
    modTemp = pd.Series(str2ndlist(Data['modTempByDepth'].values,bracket=True), index=Indx)
    
    obsILD=[] # get the ILD of the observation
    for i in Indx: 
        try:   
            if obsTemp[i][0]==obsTemp[i][1]:
                min_slope=1000  # 1000 is a large of random that represents infinity
            else:
                min_slope=abs((obsDepth[i][1]-obsDepth[i][0])/(obsTemp[i][0]-obsTemp[i][1]))
            m=0
            for k in range(1,9):
                if obsTemp[i][k]==obsTemp[i][k+1]:  
                   obsTemp[i][k+1]-=0.000000000001
                sl=abs((obsDepth[i][k+1]-obsDepth[i][k])/(obsTemp[i][k]-obsTemp[i][k+1]))
                if sl==0:
                    sl=1000
                if sl<=min_slope:
                    min_slope=sl
                    m=k
            ild=(obsDepth[i][m+1]+obsDepth[i][m])/2
        except IndexError :
            continue
        obsILD.append(ild)
    modILD=[]   #get the ILD of the mod
    for i in Indx:
        try:   
            if modTemp[i][0]==modTemp[i][1]:
                min_slope=1000  # 1000 is a large of random that represents infinity
            else:
                min_slope=abs((modDepth[i][1]-modDepth[i][0])/(modTemp[i][0]-modTemp[i][1]))
            m=0
            for k in range(1,9):
                if modTemp[i][k]==modTemp[i][k+1]:  
                   modTemp[i][k+1]-=0.000000000001
                sl=abs((modDepth[i][k+1]-modDepth[i][k])/(modTemp[i][k]-modTemp[i][k+1]))
                if sl==0:
                    sl=1000
                if sl<=min_slope:
                    min_slope=sl
                    m=k
            ild=(modDepth[i][m+1]+modDepth[i][m])/2
        except IndexError :
            continue
        modILD.append(ild)
       
    data = pd.DataFrame({'obsTime':obsTime.values, 'obsILD':obsILD, 
                        'modILD': modILD}, index=range(len(obsTime)))
    data = data.sort_index(by='obsTime')
    data.index=range(len(obsTime))
    Date=[]
    for i in data.index:
        Date.append(data['obsTime'][i])
    ave_obs=round(np.mean(obsILD),1)
    ave_mod=round(np.mean(modILD),1)
    t=[data,Date,ave_obs,ave_mod]
    T.append(t)
    print e

M,O=[],[]# smooth the model and observation ILD 
for i in range(4):
    num=6 # smooth by 6 is the best 
    ild1_smooth=utilities.smooth(T[i][0]['modILD'],num,'hanning')
    difflen1=len(ild1_smooth)-len(T[i][0]['modILD'])
    ilds1=ild1_smooth[difflen1/2:-difflen1/2]
    ild2_smooth=utilities.smooth(T[i][0]['obsILD'],num,'hanning')
    difflen2=len(ild2_smooth)-len(T[i][0]['obsILD'])
    ilds2=ild2_smooth[difflen2/2:-difflen2/2]
    M.append(ilds1)
    O.append(ilds2)
  
fig=plt.figure()
for i in range(4):
    ax = fig.add_subplot(2,2,i+1,)
    ax.plot(T[i][1], O[i], color='b', linewidth=1)#when we want to plot the smoothed 'obsILD' ,"T[i][0]['obsILD']" changed with "O[i]' 
    ax.plot(T[i][1],M[i], color='r', linewidth=1)#when we want to plot the smoothed 'modILD' ,"T[i][0]['modILD']" changed with "M[i]' 
    ax.set_title('%s'%(example[i]), fontsize=8)
    if i==2:
       dates = mpl.dates.drange(np.amin(T[i][0]['obsTime']), np.max(T[i][0]['obsTime']+timedelta(days=30)), timedelta(days=30))
    else:
       dates = mpl.dates.drange(np.amin(T[i][0]['obsTime']), np.max(T[i][0]['obsTime']), timedelta(days=30))
    dateFmt = mpl.dates.DateFormatter('%b')
    ax.set_xticks(dates)
    ax.xaxis.set_major_formatter(dateFmt)
    ax.set_ylim([35,2]) 
    plt.text(T[i][0]['obsTime'][1],31,'obsmean: '+str(T[i][2]))
    plt.text(T[i][0]['obsTime'][1],34,'modmean: '+str(T[i][3]))
    if i==1 or i==3: 
        plt.setp(ax.get_yticklabels() ,visible=False)
    if i==0 or i==1:
        plt.setp(ax.get_xticklabels() ,visible=False)
fig.text(0.5, 0.04, '2013', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Isothermal Layer Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)
#plt.savefig('ILD_4obsVSmod.png',dpi=200)
plt.show()

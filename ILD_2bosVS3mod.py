# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 15:35:00 2017
compare  isothermal layer depth(ILD) of 4 turtle data and 3 model data.
@author: yifan
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import  timedelta
from turtleModule import  str2ndlist, np_datetime
import utilities

example=[118905,117170] # those turtle's id is random  129775,,129779
T=[]  # get all information of four example turtle
for e in range(len(example)):
    obsData = pd.read_csv('ctdWithModTempByDepth.csv')
    hycom_Data = pd.read_csv('ctd_withHYCOMtemp.csv')
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
    HYCOM_Data =  hycom_Data.ix[Indx] 
    print 'len(roms_tf): ' ,len(Indx)               
    obsTime = pd.Series(np_datetime(Data['END_DATE'].values), index=Indx)
    obsTemp = pd.Series(str2ndlist(Data['TEMP_VALS'].values), index=Indx)
    obsDepth = pd.Series(str2ndlist(Data['TEMP_DBAR'].values), index=Indx)
    modTemp = pd.Series(str2ndlist(Data['modTempByDepth'].values,bracket=True), index=Indx)
    hycom_Temp = pd.Series(str2ndlist(HYCOM_Data['modtemp_HYCOM'].values, bracket=True), index=Indx)
    
    fvcom_Data = pd.read_csv('ctdWithdepthofbottom_fvcom.csv') 
    tf = np.where(fvcom_Data['in FVcom range'].notnull())[0]    # get the index of good data
    fvcom_id=pd.Series(obsData['PTT'][tf],index=tf)
    indx1=[]  
    for i in tf:
        if fvcom_id[i]==example[e]:   # we can get each turtle's ILD
            indx1.append(i)
    Temp1 = pd.Series(str2ndlist(fvcom_Data['TEMP_VALS'][indx1]), index=indx1)
    Indx1=[] # get rid of the profile without ten record points
    for i in indx1:
        if len(Temp1[i])==10:
            Indx1.append(i)
    Data1 = fvcom_Data.ix[Indx1]    
    print 'len(fvcom_tf): ' ,len(Indx1)                
    fvcom_Time = pd.Series(np_datetime(Data1['END_DATE'].values), index=Indx1)
    fvcom_Depth = pd.Series(str2ndlist(Data1['TEMP_DBAR']), index=Indx1)
    fvcom_Temp = pd.Series(str2ndlist(Data1['modtempBYdepth'], bracket=True), index=Indx1)
    
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
                min_slope=abs((obsDepth[i][1]-obsDepth[i][0])/(modTemp[i][0]-modTemp[i][1])) #
            m=0
            for k in range(1,9):
                if modTemp[i][k]==modTemp[i][k+1]:  
                   modTemp[i][k+1]-=0.000000000001
                sl=abs((obsDepth[i][k+1]-obsDepth[i][k])/(modTemp[i][k]-modTemp[i][k+1])) #
                if sl==0:
                    sl=1000
                if sl<=min_slope:
                    min_slope=sl
                    m=k
            ild=(obsDepth[i][m+1]+obsDepth[i][m])/2  #
        except IndexError :
            continue
        modILD.append(ild)
        
    hycom_ILD=[]   #get the ILD of the mod
    for i in Indx:
        try:   
            if hycom_Temp[i][0]==hycom_Temp[i][1]:
                min_slope=1000  # 1000 is a large of random that represents infinity
            else:
                min_slope=abs((obsDepth[i][1]-obsDepth[i][0])/(hycom_Temp[i][0]-hycom_Temp[i][1])) #
            m=0
            for k in range(1,9):
                if hycom_Temp[i][k]==hycom_Temp[i][k+1]:  
                   hycom_Temp[i][k+1]-=0.000000000001
                sl=abs((obsDepth[i][k+1]-obsDepth[i][k])/(hycom_Temp[i][k]-hycom_Temp[i][k+1])) #
                if sl==0:
                    sl=1000
                if sl<=min_slope:
                    min_slope=sl
                    m=k
            ild=(obsDepth[i][m+1]+obsDepth[i][m])/2  #
        except IndexError :
            continue
        hycom_ILD.append(ild)  
    
    fvcom_ILD=[]   #get the ILD of the mod
    for i in Indx1:
        try:   
            if fvcom_Temp[i][0]==fvcom_Temp[i][1]:
                min_slope=1000  # 1000 is a large of random that represents infinity
            else:
                min_slope=abs((fvcom_Depth[i][1]-fvcom_Depth[i][0])/(fvcom_Temp[i][0]-fvcom_Temp[i][1])) #
            m=0
            for k in range(1,9):
                if fvcom_Temp[i][k]==fvcom_Temp[i][k+1]:  
                   fvcom_Temp[i][k+1]-=0.000000000001
                sl=abs((fvcom_Depth[i][k+1]-fvcom_Depth[i][k])/(fvcom_Temp[i][k]-fvcom_Temp[i][k+1])) #
                if sl==0:
                    sl=1000
                if sl<=min_slope:
                    min_slope=sl
                    m=k
            ild=(fvcom_Depth[i][m+1]+fvcom_Depth[i][m])/2  #
        except IndexError :
            continue
        fvcom_ILD.append(ild)
        
    data1 = pd.DataFrame({'fvcom_Time':fvcom_Time.values, 'fvcom_ILD':fvcom_ILD}, index=range(len(fvcom_Time)))
    data1 = data1.sort_index(by='fvcom_Time')
    data1.index=range(len(fvcom_Time))
    Date1=[]
    for i in data1.index:
        Date1.append(data1['fvcom_Time'][i])
    ave_fvcom=round(np.mean(fvcom_ILD),1)
       
    data = pd.DataFrame({'obsTime':obsTime.values, 'obsILD':obsILD, 
                        'modILD': modILD,'hycom_ILD': hycom_ILD}, index=range(len(obsTime)))
    data = data.sort_index(by='obsTime')
    data.index=range(len(obsTime))
    Date=[]
    for i in data.index:
        Date.append(data['obsTime'][i])
    ave_obs=round(np.mean(obsILD),1)
    ave_mod=round(np.mean(modILD),1)
    ave_hycom=round(np.mean(hycom_ILD),1)
    t=[data,Date,ave_obs,ave_mod,ave_hycom,data1,Date1,ave_fvcom]
    T.append(t)
    print e

H,M,O,F=[],[],[],[]# smooth the model and observation ILD 
for i in range(2):
    num=6 # smooth by 6 is the best 
    ild0_smooth=utilities.smooth(T[i][0]['hycom_ILD'],num,'hanning')
    difflen0=len(ild0_smooth)-len(T[i][0]['hycom_ILD'])
    ilds0=ild0_smooth[difflen0/2:-difflen0/2]
    
    ild1_smooth=utilities.smooth(T[i][0]['modILD'],num,'hanning')
    difflen1=len(ild1_smooth)-len(T[i][0]['modILD'])
    ilds1=ild1_smooth[difflen1/2:-difflen1/2]
    
    ild2_smooth=utilities.smooth(T[i][0]['obsILD'],num,'hanning')
    difflen2=len(ild2_smooth)-len(T[i][0]['obsILD'])
    ilds2=ild2_smooth[difflen2/2:-difflen2/2]
    
    ild3_smooth=utilities.smooth(T[i][5]['fvcom_ILD'],num,'hanning')
    difflen3=len(ild3_smooth)-len(T[i][5]['fvcom_ILD'])
    ilds3=ild3_smooth[difflen3/2:-difflen3/2]
    
    H.append(ilds0)
    M.append(ilds1)
    O.append(ilds2)
    F.append(ilds3)
  
fig=plt.figure()
for i in range(2):
    ax = fig.add_subplot(2,1,i+1,)
    ax.plot(T[i][1], O[i], color='b', linewidth=1)#when we want to plot the smoothed 'obsILD' ,"T[i][0]['obsILD']" changed with "O[i]' 
    ax.plot(T[i][1],M[i], color='r', linewidth=1)#when we want to plot the smoothed 'modILD' ,"T[i][0]['modILD']" changed with "M[i]' 
    ax.plot(T[i][1], H[i], color='g', linewidth=1)
    ax.plot(T[i][6], F[i], color='k', linewidth=1)
    ax.set_title('%s'%(example[i]), fontsize=8)
    if i==0:
       dates = mpl.dates.drange(np.amin(T[i][0]['obsTime']), np.max(T[i][0]['obsTime']+timedelta(days=30)), timedelta(days=30))
    else:
       dates = mpl.dates.drange(np.amin(T[i][0]['obsTime']), np.max(T[i][0]['obsTime']), timedelta(days=30))
    dateFmt = mpl.dates.DateFormatter('%b')
    ax.set_xticks(dates)
    ax.xaxis.set_major_formatter(dateFmt)
    ax.set_ylim([42,2]) 
    plt.text(T[i][0]['obsTime'][3],29.5,'obs_mean: '+str(T[i][2]),color='b',fontsize=8)
    plt.text(T[i][0]['obsTime'][3],33,'roms_mean: '+str(T[i][3]),color='r',fontsize=8)
    plt.text(T[i][0]['obsTime'][3],36.5,'hycom_mean: '+str(T[i][4]),color='g',fontsize=8)
    plt.text(T[i][0]['obsTime'][3],40,'fvcom_mean: '+str(T[i][7]),color='k',fontsize=8)
    if i==0 :
        plt.setp(ax.get_xticklabels() ,visible=False)
fig.text(0.5, 0.04, '2013', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Isothermal Layer Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)
plt.savefig('ILD_obsVSmod_smooth_newpicture.png',dpi=200)
plt.show()

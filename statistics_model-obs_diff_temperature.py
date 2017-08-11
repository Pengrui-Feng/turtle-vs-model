# -*- coding: utf-8 -*-
'''
plot roms,fvcom and hycom quantity and ratio of error in each depth   
@author: yifan
'''
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import netCDF4
import watertempModule as wtm   # A module of classes that using ROMS, FVCOM
from turtleModule import str2ndlist, np_datetime, bottom_value, dist
#####################################ship######################################
obsData=pd.read_csv('matched_turtleVSship1.csv')
obsdepth=pd.Series(str2ndlist(obsData['turtle_depth'], bracket=True))
obstemp=pd.Series(str2ndlist(obsData['turtle_temp'], bracket=True))
shipdepth=pd.Series(str2ndlist(obsData['ship_depth'], bracket=True))
shiptemp=pd.Series(str2ndlist(obsData['ship_temp'], bracket=True))
data_ship = pd.DataFrame({'obstemp': obstemp,'shiptemp':shiptemp,'obsdepth': obsdepth,'shipdepth':shipdepth})
TEMP_ship_all=[]
TEMP_ship=[]
TEMP_ship_negivate=[]
N=[]
for i in range(50):   #depth 0~50m
    TEMP_ship.append(0)
    TEMP_ship_negivate.append(0)
    TEMP_ship_all.append(0)
    N.append(0)
    for j in data_ship.index:
        for q in range(len(data_ship['obsdepth'][j])):
            if int(data_ship['obsdepth'][j][q])==i:   
                TEMP_ship_all[i]=TEMP_ship_all[i]+1
                for k in range(len(data_ship['shipdepth'][j])):  
                    if data_ship['shipdepth'][j][k]==i:
                        if data_ship['shiptemp'][j][k]-data_ship['obstemp'][j][q]==10:
                            N[i]=N[i]+1
                        if data_ship['shiptemp'][j][k]-data_ship['obstemp'][j][q]>10:
                            TEMP_ship[i]=TEMP_ship[i]+1
                        if data_ship['obstemp'][j][q]-data_ship['shiptemp'][j][k]>10:
                            TEMP_ship_negivate[i]=TEMP_ship_negivate[i]-1
print 'all',TEMP_ship_all
print 'positive',TEMP_ship
print 'negative',TEMP_ship_negivate
print 'N',N           
#####################################roms######################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') # extracted from ctdWithModTempByDepth.py
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modTempByDepth'][tf_index], bracket=True)), index=tf_index)
data_roms = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_roms_all=[]
TEMP_roms=[]
TEMP_roms_negivate=[]
N=[]
for i in range(50):   #depth 0~50m
    TEMP_roms.append(0)
    TEMP_roms_negivate.append(0)
    TEMP_roms_all.append(0)
    N.append(0)
    for j in data_roms.index:
        for q in range(len(data_roms['depth'][j])):
            if int(data_roms['depth'][j][q])==i:   
                TEMP_roms_all[i]=TEMP_roms_all[i]+1
                if data_roms['modtemp'][j][q]<100:  #some bad data>100 degC
                    if data_roms['modtemp'][j][q]-data_roms['obstemp'][j][q]==10:
                        N[i]=N[i]+1
                    if data_roms['modtemp'][j][q]-data_roms['obstemp'][j][q]>10:
                        TEMP_roms[i]=TEMP_roms[i]+1
                    if data_roms['obstemp'][j][q]-data_roms['modtemp'][j][q]>10:
                        TEMP_roms_negivate[i]=TEMP_roms_negivate[i]-1
print 'all',TEMP_roms_all
print 'positive',TEMP_roms
print 'negative',TEMP_roms_negivate
print 'N',N
######################################fvcom####################################
obsData = pd.read_csv('ctdWithdepthofbottom_fvcom.csv') 
tf_index = np.where(obsData['in FVcom range'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtempBYdepth'][tf_index], bracket=True)), index=tf_index)
data_fvcom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_fvcom_all=[]
TEMP_fvcom=[]
TEMP_fvcom_negivate=[]
for i in range(50):   #depth 0~50m
    TEMP_fvcom.append(0)
    TEMP_fvcom_negivate.append(0)
    TEMP_fvcom_all.append(0)
    for j in data_fvcom.index:
        for q in range(len(data_fvcom['depth'][j])):
            if int(data_fvcom['depth'][j][q])==i:   
                TEMP_fvcom_all[i]=TEMP_fvcom_all[i]+1
                if -10<data_fvcom['modtemp'][j][q]<100:  #some bad data>100 degC
                    if data_fvcom['modtemp'][j][q]-data_fvcom['obstemp'][j][q]>10:
                        TEMP_fvcom[i]=TEMP_fvcom[i]+1
                    if data_fvcom['obstemp'][j][q]-data_fvcom['modtemp'][j][q]>10:
                        TEMP_fvcom_negivate[i]=TEMP_fvcom_negivate[i]-1
######################################hycom####################################  
obsData = pd.read_csv('ctd_withHYCOMtemp.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtemp_HYCOM'][tf_index], bracket=True)), index=tf_index)
data_hycom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_hycom_all=[]
TEMP_hycom=[]
TEMP_hycom_negivate=[]
for i in range(50):   #depth 0~50m
    TEMP_hycom.append(0)
    TEMP_hycom_negivate.append(0)
    TEMP_hycom_all.append(0)
    for j in data_hycom.index:
        for q in range(len(data_hycom['depth'][j])):
            if int(data_hycom['depth'][j][q])==i:   
                TEMP_hycom_all[i]=TEMP_hycom_all[i]+1
                if -10<data_hycom['modtemp'][j][q]<100:  #some bad data>100 degC
                    if data_hycom['modtemp'][j][q]-data_hycom['obstemp'][j][q]>10:
                        TEMP_hycom[i]=TEMP_hycom[i]+1
                    if data_hycom['obstemp'][j][q]-data_hycom['modtemp'][j][q]>10:
                        TEMP_hycom_negivate[i]=TEMP_hycom_negivate[i]-1 
'''
fig=plt.figure()
ax=fig.add_subplot(311)
ax.barh(range(50),TEMP_roms,color='r',label='model warmer')
ax.barh(range(50),TEMP_roms_negivate,color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-500,600])
plt.text(-200,40,'ROMS',fontsize=20)
plt.title('Quantity |modeled-observed| Temperature>10 $^\circ$C',fontsize=30)
ax1=fig.add_subplot(312)
ax1.barh(range(50),TEMP_fvcom,color='r',label='model warmer')
ax1.barh(range(50),TEMP_fvcom_negivate,color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-500,600])
plt.text(-200,40,'FVCOM',fontsize=20)
plt.ylabel('Depth(m)',fontsize=30)
ax2=fig.add_subplot(313)
ax2.barh(range(50),TEMP_hycom,color='r',label='model warmer')
ax2.barh(range(50),TEMP_hycom_negivate,color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-500,600])
plt.text(-200,40,'HYCOM',fontsize=20)
plt.xlabel('Quantity',fontsize=30)
plt.savefig('Quantity |modeled-observed| Temperature>10 $^\circ$C',dpi=200)
plt.show() 
'''
'''
# this for the 3 picture,because the ship data have too small difference with turtle,so the figure can not show
fig=plt.figure()
ax=fig.add_subplot(311)
ax.barh(range(50),np.round(np.array([float(i) for i in TEMP_roms])/np.array([float(i) for i in TEMP_roms_all])*100,3),color='r',linewidth=0.3,label='roms warmer')
ax.barh(range(50),np.round(np.array([float(i) for i in TEMP_roms_negivate])/np.array([float(i) for i in TEMP_roms_all])*100,3),color='b',linewidth=0.3,label='roms colder')
plt.legend(loc=1,fontsize = 'xx-small')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
#plt.text(-200,40,'ROMS',fontsize=20)
plt.title('modeled-observed| Temperature>10 $^\circ$C',fontsize=16)
ax1=fig.add_subplot(312)
ax1.barh(range(50),np.round(np.array([float(i) for i in TEMP_fvcom])/np.array([float(i) for i in TEMP_fvcom_all])*100,3),color='r',linewidth=0.3,label='fvcom warmer')
ax1.barh(range(50),np.round(np.array([float(i) for i in TEMP_fvcom_negivate])/np.array([float(i) for i in TEMP_fvcom_all])*100,3),color='b',linewidth=0.3,label='fvcom colder')
plt.legend(loc=1,fontsize = 'xx-small')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
#plt.text(-200,40,'FVCOM',fontsize=20)
plt.ylabel('Depth(m)',fontsize=14)
ax2=fig.add_subplot(313)
ax2.barh(range(50),np.round(np.array([float(i) for i in TEMP_hycom])/np.array([float(i) for i in TEMP_hycom_all])*100,3),color='r',linewidth=0.3,label='hycom warmer')
ax2.barh(range(50),np.round(np.array([float(i) for i in TEMP_hycom_negivate])/np.array([float(i) for i in TEMP_hycom_all])*100,3),color='b',linewidth=0.3,label='hycom colder')
plt.legend(loc=1,fontsize = 'xx-small')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
#plt.text(-200,40,'HYCOM',fontsize=20)
plt.xlabel('Percentage(%)',fontsize=14)
plt.savefig('Percentage',dpi=200)
plt.show()
'''
fig=plt.figure()
ax3=fig.add_subplot(221)
ax3.barh(range(50),np.round(np.array([float(i) for i in TEMP_ship])/np.array([float(i) for i in TEMP_ship_all])*100,3),color='r',linewidth=0.3,label='ship warmer')
ax3.barh(range(50),np.round(np.array([float(i) for i in TEMP_ship_negivate])/np.array([float(i) for i in TEMP_ship_all])*100,3),color='b',linewidth=0.3,label='ship colder')
plt.legend(loc=1,fontsize = 'xx-small')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)

ax=fig.add_subplot(222)
ax.barh(range(50),np.round(np.array([float(i) for i in TEMP_roms])/np.array([float(i) for i in TEMP_roms_all])*100,3),color='r',linewidth=0.3,label='roms warmer')
ax.barh(range(50),np.round(np.array([float(i) for i in TEMP_roms_negivate])/np.array([float(i) for i in TEMP_roms_all])*100,3),color='b',linewidth=0.3,label='roms colder')
plt.legend(loc=1,fontsize = 'xx-small')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
#plt.text(-200,40,'ROMS',fontsize=20)
#plt.title('Percentage |modeled-observed| Temperature>10 $^\circ$C',fontsize=16)
ax1=fig.add_subplot(223)
ax1.barh(range(50),np.round(np.array([float(i) for i in TEMP_fvcom])/np.array([float(i) for i in TEMP_fvcom_all])*100,3),color='r',linewidth=0.3,label='fvcom warmer')
ax1.barh(range(50),np.round(np.array([float(i) for i in TEMP_fvcom_negivate])/np.array([float(i) for i in TEMP_fvcom_all])*100,3),color='b',linewidth=0.3,label='fvcom colder')
plt.legend(loc=1,fontsize = 'xx-small')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
#plt.text(-200,40,'FVCOM',fontsize=20)
#plt.ylabel('Depth(m)',fontsize=14)
ax2=fig.add_subplot(224)
ax2.barh(range(50),np.round(np.array([float(i) for i in TEMP_hycom])/np.array([float(i) for i in TEMP_hycom_all])*100,3),color='r',linewidth=0.3,label='hycom warmer')
ax2.barh(range(50),np.round(np.array([float(i) for i in TEMP_hycom_negivate])/np.array([float(i) for i in TEMP_hycom_all])*100,3),color='b',linewidth=0.3,label='hycom colder')
plt.legend(loc=1,fontsize = 'xx-small')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
#plt.text(-200,40,'HYCOM',fontsize=20)
#plt.xlabel('Percentage(%)',fontsize=14)
fig.text(0.5, 0.04, 'Percentage(%)', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)
fig.text(0.5, 0.94, 'Comparison with turtle| Temperature>10 $^\circ$C', ha='center', va='center', fontsize=16)
plt.savefig('Percent Time',dpi=200)
plt.show()

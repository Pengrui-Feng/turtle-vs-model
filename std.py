# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 14:49:34 2017
plot 4 maps in 1 figure to show which depth has the most errors. Also plot the errorbar and ratio
Plot error bar and ratio of error in 3 models.
@author: zdong
"""

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
TEMP_ship=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_ship.append([])
    for j in data_ship.index:
        for q in range(len(data_ship['obsdepth'][j])):
            if int(data_ship['obsdepth'][j][q])==i:   #no depth<2m
                for r in range(len(data_ship['shipdepth'][j])):
                    if int(data_ship['shipdepth'][j][r])==i:
                        TEMP_ship[i].append(data_ship['shiptemp'][j][r]-data_ship['obstemp'][j][q])
print 1
#####################################roms######################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') # extracted from ctdWithModTempByDepth.py
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modTempByDepth'][tf_index], bracket=True)), index=tf_index)
data_roms = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_roms=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_roms.append([])
    for j in data_roms.index:
        for q in range(len(data_roms['depth'][j])):
            if int(data_roms['depth'][j][q])==i:   #no depth<2m
                if data_roms['modtemp'][j][q]<100:  #some bad data>100 degC
                    TEMP_roms[i].append(data_roms['modtemp'][j][q]-data_roms['obstemp'][j][q])
print 2
######################################fvcom####################################
obsData = pd.read_csv('ctdWithdepthofbottom_fvcom.csv') 
tf_index = np.where(obsData['in FVcom range'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtempBYdepth'][tf_index], bracket=True)), index=tf_index)
data_fvcom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_fvcom=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_fvcom.append([])
    for j in data_fvcom.index:
        for q in range(len(data_fvcom['depth'][j])):
            if int(data_fvcom['depth'][j][q])==i:   #no depth<2m
                if data_fvcom['modtemp'][j][q]<100:  #some bad data>100 degC
                    TEMP_fvcom[i].append(data_fvcom['modtemp'][j][q]-data_fvcom['obstemp'][j][q])
print 3
######################################hycom####################################
obsData = pd.read_csv('ctd_withHYCOMtemp.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtemp_HYCOM'][tf_index], bracket=True)), index=tf_index)
data_hycom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_hycom=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_hycom.append([])
    for j in data_hycom.index:
        for q in range(len(data_hycom['depth'][j])):
            if int(data_hycom['depth'][j][q])==i:   #no depth<2m
                if -10<data_hycom['modtemp'][j][q]<100:  #some bad data>100 and <-10 degC
                    TEMP_hycom[i].append(data_hycom['modtemp'][j][q]-data_hycom['obstemp'][j][q])
print 4
ave_roms,std_roms=[],[]
ave_ship,std_ship=[],[]
ave_fvcom,std_fvcom=[],[]
ave_hycom,std_hycom=[],[]

for i in range(50):  #depth 0~50m
    ave_roms.append(np.mean(TEMP_roms[i]))
    std_roms.append(np.std(TEMP_roms[i]))
    ave_ship.append(np.mean(TEMP_ship[i]))
    std_ship.append(np.std(TEMP_ship[i]))
    ave_fvcom.append(np.mean(TEMP_fvcom[i]))
    std_fvcom.append(np.std(TEMP_fvcom[i]))
    ave_hycom.append(np.mean(TEMP_hycom[i]))
    std_hycom.append(np.std(TEMP_hycom[i]))
fig=plt.figure()
ax=fig.add_subplot(221)
ax.errorbar(ave_ship,range(len(ave_ship)),linewidth=0.8,xerr=std_ship,elinewidth=0.5,capsize=1)
plt.ylim([50,0])
plt.xlim([-8.1,11])
plt.setp(ax.get_xticklabels() ,visible=False)
plt.text(-7,37,'SHIP',fontsize=10)
ax=fig.add_subplot(222)
ax.errorbar(ave_roms,range(len(ave_roms)),linewidth=0.8,xerr=std_roms,elinewidth=0.5,capsize=1)
plt.ylim([50,0])
plt.xlim([-8.1,11])
plt.setp(ax.get_xticklabels() ,visible=False)
plt.setp(ax.get_yticklabels() ,visible=False)
plt.text(-7,37,'ROMS',fontsize=10)
#plt.title('Modeled-observed at multiple levels',fontsize=20)
ax1=fig.add_subplot(223)
ax1.errorbar(ave_fvcom,range(len(ave_fvcom)),linewidth=0.8,xerr=std_fvcom,elinewidth=0.5,capsize=1)
plt.ylim([50,0])
plt.xlim([-8.1,11])
plt.text(-7,37,'FVCOM',fontsize=10)
ax2=fig.add_subplot(224)
ax2.errorbar(ave_hycom,range(len(ave_hycom)),linewidth=0.8,xerr=std_hycom,elinewidth=0.5,capsize=1)
plt.ylim([50,0])
plt.xlim([-8.1,11])
plt.setp(ax2.get_yticklabels() ,visible=False)
plt.text(-7,37,'HYCOM',fontsize=10)
fig.text(0.5, 0.04, 'Temperature ($^\circ$C)', ha='center', va='center', fontsize=14)#  0.5 ,0.04 represent the  plotting scale of x_axis and y_axis
fig.text(0.06, 0.5, 'Depth(m)', ha='center', va='center', rotation='vertical',fontsize=14)
fig.text(0.5, 0.94, 'comparison with turtle data', ha='center', va='center', fontsize=16)
plt.savefig('comparison with turtle data.png',dpi=200)
plt.show()
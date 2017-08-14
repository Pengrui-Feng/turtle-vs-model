 # -*- coding: utf-8 -*-
"""
'plot number of dive and turtle in each month'
Created on Tue Feb  3 09:07:00 2015
@author: zhaobin
some modifications by JiM in Jan 2016
where I added #CTD profiles as well
some some modifications by yifan in july 2017
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,np_datetime
####################################################
obsData=pd.read_csv('ctdWithModTempByDepth.csv') # this is actually the turtle data
tf_index=np.where(obsData['TF'].notnull())[0] # finds index of good data
obsTime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]), index=tf_index) # makes Pandas Series
turtle_ids = pd.Series(obsData['PTT'])
Num=[]
num=[[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]]]
#num is 5*12,5 is 5 years,12 is 12 months
for i in range(5):    # 2009~2013,5 years
    Num.append([0]*12)    #12 months
for i in tf_index: # loop through all the profiles
    for j in range(5): # loop through all the years
        if obsTime[i].year==2009+j: # for this year
            for q in range(12):
                if obsTime[i].month==q+1: # if in this month
                    Num[j][q]+=1 # keep track of how many in this month and this year
                    num[j][q].append(i) # adds the index for this month and this year
for i in range(len(num)):
    for j in range(len(num[i])):
        num[i][j]=len(turtle_ids[num[i][j]].unique()) # this is only needed for the 2nd figure w/#of turtles

width=0.2
color=['blue','black','red','green','yellow']

# now plot the number of turtle  profiles per month on one panel and CTD profiles on another
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

for i in range(5):
    ax1.bar(np.arange(1,13)+width*(i-2),Num[i],align="center",width=width,color=color[i] ,label=str(i+2009))
#ax1.legend(loc='best')
ax1.set_xlim([1,13]) 
ax1.set_xticks(range(1,13))
#ax1.set_yticklabels(fontsize=18)
#ax1.set_xlabel('Month',fontsize=20)
ax1.set_ylabel('Quantity',fontsize=16)
ax1.tick_params(labelsize=10)
ax1.set_title('#Turtle profiles per month',fontsize=12)

# now plot the number of CTD profiles per month
fin=open('count_casts_by_latlon.lst','r') # this is the output of an sql program of the same name
lines=fin.readlines()
y=-1
numctd=[[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]]]
for m in range(len(lines)-1): # loop through the whole file one line at a time
     if  len(lines[m])>1:
          if lines[m][0]=='S': # means start of a month
               y=y+1
               for k in range(12):
                 numctd[y][k]=int(lines[m+k*2+1]) # counts the number of CTD in this year and this month
#fig=plt.figure()
for i in range(5):
    ax2.bar(np.arange(1,13)+width*(i-2),numctd[i],align="center",width=width,color=color[i] ,label=str(i+2009))
ax2.legend(loc='best',fontsize='small')
ax2.set_xlim([1,13]) 
ax2.set_xticks(range(1,13))
#ax2.yticks(fontsize=18)
#ax2.set_xlabel('Month',fontsize=20)
f.text(0.5,0.04,'Month',ha='center', va='center',fontsize=16)
#f.text(0.06,0.5,'Month',ha='center', va='center',rotation='vertical',fontsize=16)
ax2.tick_params(labelsize=10)
#ax2.ylabel('Quantity',fontsize=20)
ax2.set_title('#Ship profiles per month',fontsize=12)
plt.savefig('thenumberofprofiles_turtleVSship_permonth.png',dpi=200)#/net/pubweb_html/epd/ocean/MainPage/turtle/
'''
# now plot the number of turtles per month
fig = plt.figure()
for i in range(5):
    plt.bar(np.arange(1,13)+width*(i-2),num[i],align="center",width=width,color=color[i] ,label=str(i+2009))
plt.legend(loc='best')
plt.xlim([0,13]) 
plt.xticks(range(13),fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel('month',fontsize=20)
plt.ylabel('quantity',fontsize=20)
plt.title('Number of turtle',fontsize=20)
plt.show()
'''

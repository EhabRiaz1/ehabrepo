###############################################################################
###############################################################################
import pandas as pd
import numpy as np
from yf_data_download import month_df

import os
os.getcwd() #know your work directory
# os.chdir('./') #set your work directory, e.g. C:/Users/c0000000
os.chdir('/Users/ehabriaz/Desktop/pytonbacktest')

###############################################################################
###############################################################################

###############################################################################
###############################################################################
def transform(x,freq='1min',usecol='Adj Close'):
    # transform the original data to nxm
    # n is the number of trading days
    # m is the number of price bars per day
    sd = np.min(x.index)
    ed = np.max(x.index)
    date_index = pd.date_range(start=sd,end=ed, freq='D') #create a date index series
    time_index = pd.date_range(pd.to_datetime('09:30:00', format="%H:%M:%S"),pd.to_datetime('15:59:59', format="%H:%M:%S"), freq=freq)
    x_dates = np.array(list(map(lambda x : x.date(),x.index)))
    x_mat = pd.DataFrame(index=date_index,columns=time_index.time)
    for d in date_index:
    # Import data by yourself
        day1_ind = (x_dates==d.date()) #find all index (boolean) on d
        if np.sum(day1_ind)>0:
            day1_x = x[usecol][day1_ind]
            x_mat.loc[d,day1_x.index.time] = day1_x.values
    x_mat.dropna(how='all',inplace=True)
    return x_mat
###############################################################################
###############################################################################


###############################################################################
###############################################################################
def fill_missing_dat(filledData):
    
    #Forward fill missing values 
    filledData.fillna(method = 'ffill', inplace = True )
    
    #backward fill missing values 
    filledData.fillna(method = 'bfill', inplace = True)
    
    #Linearly interpolate an missing values
    filledData.interpolate(method='linear', limit_direction='both', inplace=True)
    
    return filledData
###############################################################################
###############################################################################

dat = pd.read_csv('Amzn_13-11_lastMonth.csv',parse_dates=['Datetime'],index_col='Datetime')
ret = np.diff(np.log(month_df['Adj Close'])) #log-returns
dat.shape[0] #number of observations. Is it correct?
m = 6.5*60 #number of 1-min volumes per day
''' Transfer to daily data table '''

''' Some intraday data properties'''
# Find return table
# ret_mat = ???
# # Find intraday volume table
# volume_mat = ???

# ''' Some plots '''
# from matplotlib import pyplot as plt
# plt.plot(volume_mat.mean(axis=0).values)






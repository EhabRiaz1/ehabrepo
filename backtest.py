# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:02:11 2022

@author: pastor&benji
"""

import pandas as pd
import numpy as np
import technical_indicator as tech
import preanalysis as pre

import os
os.getcwd() #know your work directory
os.chdir('./') #set your work directory, e.g. C:/Users/c0000000

''' Define functions for backtest analysis '''
def cntTrades(signal):
    #find the number of trades in each day
    change_position = signal.copy().diff(axis=1)
    if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
        #long only strategy
        return np.sum(change_position>0,axis=1)
    if (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
        #short only strategy
        return np.sum(change_position<0,axis=1)
    # long-short strategy - challenge!!!
    return 

def calTotRet(p,signal):
    # p - transaction price
    # signal - position holding signal
    #find the number of trades in each day
    change_position = signal.copy().diff(axis=1)
    ret = np.zeros(p.shape[0])
    if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
        #long only strategy
        ind_in = np.where((change_position==1).values)
        ind_out = np.where((change_position==-1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.sum(np.log(p_out/p_in))
        return ret
    if (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
        #short only strategy
        ind_in = np.where((change_position==-1).values)
        ind_out = np.where((change_position==1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.sum(np.log(p_out/p_in))
        return ret
    # long-short strategy - challenge!!!
    return ret

''' prepare your data '''
file_name = 'GE_1m.csv' #this is the csv file of (merged) intraday data
dat = pd.read_csv(file_name,parse_dates=['Datetime'],index_col='Datetime')
trans_dat = pre.transform(dat) #use the function written in "preanalysis"
trans_dat=trans_dat.astype('float') #fix the data type is necessary
fixed_trans_dat = pre.fill_missing_dat(trans_dat)

''' sample cade: backtest SMA (1-min data) '''
holding = 'long' #a long-only strategy
look_back = 15 #look-back window size
sma_value,sma_signal = tech.SMA(fixed_trans_dat,window=look_back,signal_type=holding)
#create an analysis table
cols = ['Num.Obs.', 'Num.Trade', 'Tot.Ret', 'Std.Ret', 'Tot.PnL', 'Win.Ratio'] #add addtional fields if necessary
backtest_rs = pd.DataFrame(index = fixed_trans_dat.index, columns=cols)
backtest_rs['Num.Obs.'] = np.sum(~np.isnan(trans_dat),axis=1)
backtest_rs['Num.Trade'] = cntTrades(sma_signal)
backtest_rs['Tot.Ret'] = calTotRet(fixed_trans_dat,sma_signal)
backtest_rs['Std.Ret'] = ???
backtest_rs['Tot.PnL'] = ???
backtest_rs['Win.Ratio'] = ???
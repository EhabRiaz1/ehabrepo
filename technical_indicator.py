# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:16:52 2022

@author: pastor&benji
"""

import pandas as pd
import numpy as np

''' Define some technical indicators '''
def SMA(p,window=10,signal_type='long'):
    # p - price used for SMA, the nxm DataFrame
    # window - look-back window size
    # signal_type - long (default), short, or both (not recommended)
    signal = pd.DataFrame(index=p.index,columns=p.columns)
    sma = pd.DataFrame(index=p.index,columns=p.columns)
    for i in window+np.arange(p.shape[1]-window):
        #loop each column for all dates
        sma[p.columns[i]] = np.mean(p.iloc[:,(i-window):(i-1)],axis=1)
    if signal_type=='long':
        signal = (sma<p)*1 #1 for holding a long position
    elif signal_type=='short':
        signal = (sma>p)(-1) #-1 for holding a short position
    elif signal_type=='both':
        signal = (sma<p)*1+(sma>p)(-1)
    signal.iloc[:,-1]=0 #always close position at the market close
    # return sma and the signal DataFrames, both nxm
    return sma, signal

########## define more technical indicators by yourself ##########
sma_df, signal_df = SMA(X, window=10, signal_type='long')
    
########## define more technical indicators by yourself ##########
    


def RSI(p, period=14, signal_type='long'):
    # p - price used for RSI, the nxm DataFrame
    # period - look-back period size for RSI calculation
    # signal_type - long (default), short, or both (not recommended)
    signal = pd.DataFrame(index=p.index,columns=p.columns)
    rsi = pd.DataFrame(index=p.index,columns=p.columns)
    for i in period+np.arange(p.shape[1]-period):
        #loop each column for all dates
        price_change = p.iloc[:,i]-p.iloc[:,i-period]
        positive_changes = price_change.where(price_change > 0, 0)
        negative_changes = price_change.where(price_change < 0, 0)
        avg_gain = positive_changes.mean(axis=1)
        avg_loss = negative_changes.abs().mean(axis=1)
        rs = avg_gain / avg_loss
        rsi.iloc[:,i] = 100 - (100 / (1 + rs))
    if signal_type=='long':
        signal = (rsi<30)*1 #1 for holding a long position
    elif signal_type=='short':
        signal = (rsi>70)*(-1) #-1 for holding a short position
    signal.iloc[:,-1]=0 #always close position at the market close
    # return rsi and the signal DataFrames, both nxm
    return rsi, signal






# Load your DataFrame and select the 5th column as the AMZN adjusted close price



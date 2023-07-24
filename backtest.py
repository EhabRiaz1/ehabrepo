###############################################################################
###############################################################################
import pandas as pd
import numpy as np
# import technical_indicator as tech
from technical_indicator import SMA, RSI
from preanalysis import transform, fill_missing_dat

###############################################################################
###############################################################################
import os
os.getcwd() #know your work directory
os.chdir('/Users/ehabriaz/Desktop/pytonbacktest')
###############################################################################
###############################################################################



###############################################################################
################################DEFINE LOT SIZE################################
lotSz = 130
###############################################################################
###############################################################################

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
###############################################################################

# def winRat(p, signal):
#     # p - transaction price
#     # signal - position holding signal
#     change_position = signal.copy().diff(axis=1)
#     ret = np.zeros(p.shape[0])
#     cnt_win = np.zeros(p.shape[0])
#     cntWinRat = np.zeros(p.shape[0])
#     cnt_trade = cntTrades(signal)
#     for i in np.arange(p.shape[0]):
#         if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
#             #long only strategy
#             ind_in = np.where((change_position==1).values)
#             ind_out = np.where((change_position==-1).values)
#             p_in=p.values[i,ind_in[1][ind_in[0]==i]]
#             p_out=p.values[i,ind_out[1][ind_out[0]==i]]
#             ret[i] = np.sum(p_out-p_in)
#             cnt_win[i] = np.sum(p_out-p_in>0)
#             cntWinRat[i] = cnt_win[i]/cnt_trade[i]
#         elif (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
#             #short only strategy
#             ind_in = np.where((change_position==-1).values)
#             ind_out = np.where((change_position==1).values)
#             p_in=p.values[i,ind_in[1][ind_in[0]==i]]
#             p_out=p.values[i,ind_out[1][ind_out[0]==i]]
#             ret[i] = np.sum(p_in-p_out)
#             cnt_win[i] = np.sum(p_in-p_out>0)
#             cntWinRat[i] = cnt_win[i]/cnt_trade[i]
#         else:
#             # long-short strategy
#             ind_long_in = np.where((change_position==1).values)
#             ind_long_out = np.where((change_position==-1).values)
#             ind_short_in = np.where((change_position==-1).values)
#             ind_short_out = np.where((change_position==1).values)
#             p_long_in=p.values[i,ind_long_in[1][ind_long_in[0]==i]]
#             p_long_out=p.values[i,ind_long_out[1][ind_long_out[0]==i]]
#             p_short_in=p.values[i,ind_short_in[1][ind_short_in[0]==i]]
#             p_short_out=p.values[i,ind_short_out[1][ind_short_out[0]==i]]
#             ret_long = np.sum(p_long_out-p_long_in)
#             ret_short = np.sum(p_short_in-p_short_out)
#             cnt_win_long = np.sum(p_long_out-p_long_in>0)
#             cnt_win_short = np.sum(p_short_in-p_short_out>0)
#             cnt_win = cnt_win_long + cnt_win_short
#             cntWinRat[i] = cnt_win/cnt_trade[i]
#             ret[i] = ret_long + ret_short
#     return cntWinRat*100

def winRat(p,signal):
    # p - transaction price
    # signal - position holding signal
    # find the number of trades in each day
    change_position = signal.copy().diff(axis=1)
    win = np.zeros(p.shape[0])
    loss = np.zeros(p.shape[0])
    if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
        #long only strategy
        ind_in = np.where((change_position==1).values)
        ind_out = np.where((change_position==-1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret = p_out/p_in-1
            win[i] = np.sum(ret>0)
            loss[i] = np.sum(ret<0)
    if (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
        #short only strategy
        ind_in = np.where((change_position==-1).values)
        ind_out = np.where((change_position==1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret = p_out/p_in-1
            win[i] = np.sum(ret<0)
            loss[i] = np.sum(ret>0)
    # long-short strategy - challenge!!!
    return 100*win/(win+loss)




###############################################################################

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
###############################################################################

# def calTotRet(p,signal):
#     # p - transaction price
#     # signal - position holding signal
#     #find the number of trades in each day
#     change_position = signal.copy().diff(axis=1)
#     ret = np.zeros(p.shape[0])
#     if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
#         #long only strategy
#         ind_in = np.where((change_position==1).values)
#         ind_out = np.where((change_position==-1).values)
#         for i in np.arange(p.shape[0]):
#             p_in = p.values[i, ind_in[1][ind_in[0] == i]].squeeze()
#             p_out = p.values[i, ind_out[1][ind_out[0] == i]].squeeze()
#             # sort the p_in and p_out arrays by the column index
#             ind_in_sorted = np.argsort(ind_in[1][ind_in[0] == i])
#             ind_out_sorted = np.argsort(ind_out[1][ind_out[0] == i])
#             ret[i] = np.sum(np.log(p_out[ind_out_sorted] / p_in[ind_in_sorted]))
#         return ret
#     if (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
#         #short only strategy
#         ind_in = np.where((change_position==-1).values)
#         ind_out = np.where((change_position==1).values)
#         for i in np.arange(p.shape[0]):
#             p_in = p.values[i, ind_in[1][ind_in[0] == i]].squeeze()
#             p_out = p.values[i, ind_out[1][ind_out[0] == i]].squeeze()
#             # sort the p_in and p_out arrays by the column index
#             ind_in_sorted = np.argsort(ind_in[1][ind_in[0] == i])
#             ind_out_sorted = np.argsort(ind_out[1][ind_out[0] == i])
#             ret[i] = np.sum(np.log(p_out[ind_out_sorted] / p_in[ind_in_sorted]))
#         return ret
#     # long-short strategy - challenge!!!
#     return ret



###############################################################################

def calTotPnL(p, signal):
    # p - transaction price
    # signal - position holding signal
    change_position = signal.copy().diff(axis=1)
    ret = np.zeros(p.shape[0])
    if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
        #long only strategy
        ind_in = np.where((change_position==1).values)
        ind_out = np.where((change_position==-1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.sum(p_out-p_in)
        return ret
    if (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
        #short only strategy
        ind_in = np.where((change_position==-1).values)
        ind_out = np.where((change_position==1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.sum(p_in-p_out)
        return ret
    # long-short strategy - challenge!!!
    return ret
###############################################################################
###############################################################################
def calStdRet(p, signal):
    change_position = signal.copy().diff(axis=1)
    ret = np.zeros(p.shape[0])
    if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
        #long only strategy
        ind_in = np.where((change_position==1).values)
        ind_out = np.where((change_position==-1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.mean(p_out / p_in - 1)
        return ret
    if (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
        #short only strategy
        ind_in = np.where((change_position==-1).values)
        ind_out = np.where((change_position==1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.mean(p_in / p_out - 1)
        return ret
    # long-short strategy - challenge!!!
    return ret

###############################################################################
###############################################################################

# def winRat(p,signal):
#     # p - transaction price
#     # signal - position holding signal
#     #find the number of trades in each day
#     change_position = signal.diff(axis=1).values
#     n_trades = np.count_nonzero(change_position, axis=1)
#     n_wins = np.zeros(p.shape[0])
#     for i in range(p.shape[0]):
#         ind_in = np.where(change_position[i,:] == 1)[0]
#         ind_out = np.where(change_position[i,:] == -1)[0]
#         if len(ind_in) > 0 and len(ind_out) > 0:
#             # calculate the returns for each trade
#             for j in range(len(ind_in)):
#                 p_in = p.values[i, ind_in[j]]
#                 p_out = p.values[i, ind_out[j]]
#                 if p_out > p_in:
#                     n_wins[i] += 1
#     # calculate the win ratio
#     win_ratio = 100*np.sum(n_wins) / np.sum(n_trades)
#     return win_ratio

###############################################################################
###############################################################################

def calPnlLotSz(p, signal, lot_size):
    # p - transaction price
    # signal - position holding signal
    # lot_size - number of shares bought for each trade signal
    change_position = signal.copy().diff(axis=1)
    ret = np.zeros(p.shape[0])
    if (np.sum(signal.values>0)>0) and (np.sum(signal.values<0)==0):
        #long only strategy
        ind_in = np.where((change_position==1).values)
        ind_out = np.where((change_position==-1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.sum((p_out-p_in)*lot_size)
        return ret
    if (np.sum(signal.values<0)>0) and (np.sum(signal.values>0)==0):
        #short only strategy
        ind_in = np.where((change_position==-1).values)
        ind_out = np.where((change_position==1).values)
        for i in np.arange(p.shape[0]):
            p_in=p.values[i,ind_in[1][ind_in[0]==i]]
            p_out=p.values[i,ind_out[1][ind_out[0]==i]]
            ret[i] = np.sum((p_in-p_out)*lot_size)
        return ret
    # long-short strategy - challenge!!!
    return ret




def calAvgTradeDuration(signal):
    # change position
    change_position = signal.diff(axis=1)

    # find buy and sell indices
    buy_indices = np.where(change_position == 1)
    sell_indices = np.where(change_position == -1)

    # calculate trade durations
    trade_durations = []
    for i in range(len(buy_indices[1])):
        buy_index = buy_indices[1][i]
        sell_index = sell_indices[1][np.argmax(sell_indices[1] > buy_index)]
        if sell_index > buy_index:
            trade_duration = sell_index - buy_index
            trade_durations.append(trade_duration)

    # calculate average trade duration
    if len(trade_durations) > 0:
        avg_trade_duration = sum(trade_durations) / len(trade_durations)
    else:
        avg_trade_duration = 0

    return avg_trade_duration




###############################################################################
###############################################################################
###############################################################################
###############################################################################


''' Generate Transposed Data'''
file_name = 'Amzn_13-11_lastMonth.csv' #this is the csv file of (merged) intraday data
dat = pd.read_csv(file_name,parse_dates=['Datetime'],index_col='Datetime')
trans_dat = transform(dat) #use the function written in "preanalysis"
trans_dat=trans_dat.astype('float') #fix the data type is necessary
fixed_trans_dat = fill_missing_dat(trans_dat)

###############################################################################
###############################################################################
###############################################################################
###############################################################################



###############################################################################
###########################Call Technical Indicator############################
######################################SMA######################################
###############################################################################



''' sample cade: backtest SMA (1-min data) '''
holding = 'long' #a long-only strategy
look_back = 9 #look-back window size
sma_value,sma_signal,pos = SMA(fixed_trans_dat,window=look_back,signal_type=holding)
###############################################################################
cols = ['Num.Obs.', 'Num.Trade', 'Tot.Ret', 'Std.Ret', 'Tot.PnL', 'Win.Ratio', 'P/L.LOTSZ', 'AVG.Time'] #add addtional fields if necessary
backtestSMA = pd.DataFrame(index = fixed_trans_dat.index, columns=cols)
backtestSMA['Num.Obs.'] = np.sum(~np.isnan(trans_dat),axis=1)
backtestSMA['Num.Trade'] = cntTrades(sma_signal)
backtestSMA['Tot.Ret'] = calTotRet(fixed_trans_dat,pos)
backtestSMA['Std.Ret'] = calStdRet(fixed_trans_dat,pos)
backtestSMA['Tot.PnL'] = calTotPnL(fixed_trans_dat, pos)
backtestSMA['Win.Ratio'] = winRat(fixed_trans_dat,pos)
backtestSMA['P/L.LOTSZ'] = calPnlLotSz(fixed_trans_dat,pos, lotSz)
backtestSMA['AVG.Time'] = calAvgTradeDuration(pos)


###############################################################################
###########################Call Technical Indicator############################
######################################RSI######################################
###############################################################################
'''Calling RSI Signal'''
holding = 'long'
valuesRSI, signalRSI, posRSI = RSI(fixed_trans_dat, period=9, signal_type=holding)
###############################################################################

cols = ['Num.Obs.', 'Num.Trade', 'Tot.Ret', 'Std.Ret', 'Tot.PnL', 'Win.Ratio', 'P/L.LOTSZ', 'AvgTime'] #add addtional fields if necessary
backtestRSI = pd.DataFrame(index = fixed_trans_dat.index, columns=cols)
backtestRSI['Num.Obs.'] = np.sum(~np.isnan(trans_dat),axis=1)
backtestRSI['Num.Trade'] = cntTrades(posRSI)
backtestRSI['Tot.Ret'] = calTotRet(fixed_trans_dat,posRSI)
backtestRSI['Std.Ret'] = calStdRet(fixed_trans_dat,posRSI)
backtestRSI['Tot.PnL'] = calTotPnL(fixed_trans_dat, posRSI)
backtestRSI['Win.Ratio'] = winRat(fixed_trans_dat,posRSI)
backtestRSI['P/L.LOTSZ'] = calPnlLotSz(fixed_trans_dat,posRSI, lotSz)
backtestRSI['AvgTime'] = calAvgTradeDuration(posRSI)
backtestRSI.to_csv('backtestRSI.csv')


###############################################################################
###############################################################################
###############################################################################
###############################################################################



# '''Calling EMA Signal'''
# holding = 'long'
# valuesEMA10, valueEMA5,signalEMA = EMA(fixed_trans_dat, period=17, signal_type=holding)
# ###############################################################################

# cols = ['Num.Obs.', 'Num.Trade', 'Tot.Ret', 'Std.Ret', 'Tot.PnL', 'Win.Ratio', 'P/L.LOTSZ', 'AvgTime'] #add addtional fields if necessary
# backtestEMA = pd.DataFrame(index = fixed_trans_dat.index, columns=cols)
# backtestEMA['Num.Obs.'] = np.sum(~np.isnan(trans_dat),axis=1)
# backtestEMA['Num.Trade'] = cntTrades(signalEMA)
# backtestEMA['Tot.Ret'] = calTotRet(fixed_trans_dat,signalEMA)
# backtestEMA['Std.Ret'] = calStdRet(fixed_trans_dat,signalEMA)
# backtestEMA['Tot.PnL'] = calTotPnL(fixed_trans_dat, signalEMA)
# backtestEMA['Win.Ratio'] = winRat(fixed_trans_dat,signalEMA)
# backtestEMA['P/L.LOTSZ'] = calPnlLotSz(fixed_trans_dat,signalEMA, lotSz)
# backtestEMA['AvgTime'] = calAvgTradeDuration(signalEMA)

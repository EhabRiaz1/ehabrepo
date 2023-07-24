###############################################################################
###############################################################################
import pandas as pd
import numpy as np
import os 

os.getcwd()
os.chdir('/Users/ehabriaz/Desktop/pytonbacktest')



###############################################################################
###############################################################################
###############################################################################
###############################################################################



###############################################################################

def SMA(p, window=10, signal_type='long'):
    # p - price used for SMA, the nxm DataFrame
    # window - look-back window size
    # signal_type - long (default), short, or both (not recommended)
    signal = pd.DataFrame(index=p.index,columns=p.columns)
    sma = pd.DataFrame(index=p.index,columns=p.columns)
    pos = pd.DataFrame(index=p.index,columns=p.columns)
    for i in window+np.arange(p.shape[1]-window):
        # loop each column for all dates
        sma[p.columns[i]] = np.mean(p.iloc[:,(i-window):(i-1)],axis=1)
    if signal_type=='long':
        signal = (p < sma) * 1 # 1 for holding a long position
        pos = (p < sma) * 1 # set position to long
    elif signal_type=='short':
        signal = (p > sma) * -1 #-1 for holding a short position
        pos = (p > sma) * -1 # set position to short
    elif signal_type=='both':
        signal_long = (p < sma) * 1 # 1 for holding a long position
        signal_short = (p > sma) * -1 #-1 for holding a short position
        signal = signal_long + signal_short
        pos = signal_long + signal_short # set position to long or short
        pos[pos == -2] = -1 # combine long and short positions
    signal.iloc[:,-1] = 0 # always close position at the market close
    pos.iloc[:,-1] = 0 # always close position at the market close
    # additional criteria for closing positions
    for i in range(window+1, p.shape[0]):
        for j in range(p.shape[1]):
            # check if the position is open
            if pos.iloc[i-1,j] != 0:
                # check if the price has dropped by more than 7%
                if (p.iloc[i,j] / p.iloc[i-window-1,j]) < 0.93:
                    pos.iloc[i,j] = 0 # close the position
                # check if the last 3 SMA values have been decreasing
                elif (sma.iloc[i-1,j] < sma.iloc[i-2,j]) and (sma.iloc[i-2,j] < sma.iloc[i-3,j]):
                    pos.iloc[i,j] = 0 # close the position
        

    return sma, signal, pos


###############################################################################

# def RSI(p, period=3, signal_type='long'):
#     # p - price used for RSI, the nxm DataFrame
#     # period - look-back period size for RSI calculation
#     # signal_type - long (default), short, or both (not recommended)
#     signal = pd.DataFrame(index=p.index,columns=p.columns)
#     rsi = pd.DataFrame(index=p.index,columns=p.columns)
#     for idx in p.index:
#         price_changes = p.loc[idx].diff(periods=1)
#         positive_changes = price_changes.where(price_changes > 0, 0)
#         negative_changes = price_changes.where(price_changes < 0, 0)
#         avg_gain = positive_changes.rolling(window=period).mean()
#         avg_loss = negative_changes.abs().rolling(window=period).mean()
#         rs = avg_gain / avg_loss
#         rsi_val = 100 - (100 / (1 + rs))
#         rsi.loc[idx] = rsi_val
#     if signal_type=='long':
#         signal = (rsi<30)*1 #1 for holding a long position
#     elif signal_type=='short':
#         signal = (rsi>70)*(-1)
#     elif signal_type == 'both':
#         signal = (rsi<30)*1
#         signal = (rsi>70)*-1#-1 for holding a short position
#     signal.iloc[:,-1]=0 #always close position at the market close
#     # return rsi and the signal DataFrames, both nxm
#     return rsi, signal


def RSI(p, period=3, signal_type='long'):
    # p - price used for RSI, the nxm DataFrame
    # period - look-back period size for RSI calculation
    # signal_type - long (default), short, or both (not recommended)
    signal = pd.DataFrame(index=p.index,columns=p.columns)
    rsi = pd.DataFrame(index=p.index,columns=p.columns)
    pos = pd.DataFrame(index=p.index,columns=p.columns)
    for idx in p.index:
        price_changes = p.loc[idx].diff(periods=1)
        positive_changes = price_changes.where(price_changes > 0, 0)
        negative_changes = price_changes.where(price_changes < 0, 0)
        avg_gain = positive_changes.rolling(window=period).mean()
        avg_loss = negative_changes.abs().rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi_val = 100 - (100 / (1 + rs))
        rsi.loc[idx] = rsi_val
    if signal_type=='long':
        signal = (rsi<20)*1 #1 for holding a long position
        pos = (rsi<30)*1 #set position to long
    elif signal_type=='short':
        signal = (rsi>90)*(-1)
        pos = (rsi>70)*(-1) #set position to short
    elif signal_type == 'both':
        signal_long = (rsi<30)*1
        signal_short = (rsi>70)*-1 #-1 for holding a short position
        signal = signal_long + signal_short
        pos = signal_long + signal_short #set position to long or short
        pos[pos == -2] = -1 #combine long and short positions
    signal.iloc[:,-1]=0 #always close position at the market close
    pos.iloc[:,-1]=0 #always close position at the market close
    #additional criteria for closing positions
    for i in range(period+1, p.shape[0]):
        for j in range(p.shape[1]):
            #check if the position is open
            if pos.iloc[i-1,j] != 0:
                #check if the price has dropped by more than 7%
                if (p.iloc[i,j] / p.iloc[i-period-1,j]) < 0.99:
                    pos.iloc[i,j] = 0 #close the position
    return rsi, signal, pos

###############################################################################
###############################################################################
# def EMA(p, window=10, signal_type='long'):
#     # p - price used for EMA, the nxm DataFrame
#     # window - look-back window size
#     # signal_type - long (default), short, or both (not recommended)
#     signal = pd.DataFrame(index=p.index,columns=p.columns)
#     ema = pd.DataFrame(index=p.index,columns=p.columns)
#     pos = pd.DataFrame(index=p.index,columns=p.columns)
    
#     alpha = 2 / (window + 1) # compute alpha for EMA
    
#     ema = p.ewm(alpha=alpha, min_periods=window).mean() # compute EMA for each column
    
#     if signal_type=='long':
#         signal = (p < ema) * 1 # 1 for holding a long position
#         pos = (p < ema) * 1 # set position to long
#     elif signal_type=='short':
#         signal = (p > ema) * -1 #-1 for holding a short position
#         pos = (p > ema) * -1 # set position to short
#     elif signal_type=='both':
#         signal_long = (p < ema) * 1 # 1 for holding a long position
#         signal_short = (p > ema) * -1 #-1 for holding a short position
#         signal = signal_long + signal_short
#         pos = signal_long + signal_short # set position to long or short
#         pos[pos == -2] = -1 # combine long and short positions
        
#     signal.iloc[:,-1] = 0 # always close position at the market close
#     pos.iloc[:,-1] = 0 # always close position at the market close
    
#     # additional criteria for closing positions
#     for i in range(window+1, p.shape[0]):
#         for j in range(p.shape[1]):
#             # check if the position is open
#             if pos.iloc[i-1,j] != 0:
#                 # check if the price has dropped by more than 7%
#                 if (p.iloc[i,j] / p.iloc[i-window-1,j]) < 0.93:
#                     pos.iloc[i,j] = 0 # close the position
#                 # check if the last 3 EMA values have been decreasing
#                 elif (ema.iloc[i-1,j] < ema.iloc[i-2,j]) and (ema.iloc[i-2,j] < ema.iloc[i-3,j]):
#                     pos.iloc[i,j] = 0 # close the position

#     return ema, signal, pos


###############################################################################
###############################################################################
# def EMA(p, period=3, signal_type='long'):
#     # # p - price used for EMA, the nxm DataFrame
#     # # period - look-back period size for EMA calculation
#     # # signal_type - long (default), short, or both (not recommended)
#     # signal = pd.DataFrame(index=p.index,columns=p.columns)
#     # ema = pd.DataFrame(index=p.index,columns=p.columns)
#     # for idx in p.index:
#     #     ema_valTen = p.loc[idx].ewm(span=10, min_periods=period).mean()
#     #     emaTen.loc[idx] = ema_valTen
#     #     ema_valFive = p.loc[idx].ewm(span=5, min_periods=period).mean()
#     #     emaFive.loc[idx] = ema_valFive
#     # if signal_type=='long':
#     #     signal = (ema_valTen>ema_valFive) & (p>ema)*1 #1 for holding a long position
#     # elif signal_type=='short':
#     #     signal = (p<ema)*(-1) #-1 for holding a short position
#     # signal.iloc[:,-1]=0 #always close position at the market close

#         # p - price used for EMA, the nxm DataFrame
#         # period - look-back period size for EMA calculation
#         # signal_type - long (default), short, or both (not recommended)
#         signal = pd.DataFrame(index=p.index,columns=p.columns)
#         emaTen = pd.DataFrame(index=p.index,columns=p.columns)
#         emaFive = pd.DataFrame(index=p.index,columns=p.columns)        for idx in p.index:
#             ema_valTen = p.loc[idx].ewm(span=10, min_periods=period).mean()
#             emaTen.loc[idx] = ema_valTen
#             ema_valFive = p.loc[idx].ewm(span=5, min_periods=period).mean()
#             emaFive.loc[idx] = ema_valFive
#         if signal_type=='long':
#             signal = (ema_valTen>ema_valFive) & (p>ema)*1 #1 for holding a long position
#         elif signal_type=='short':
#             signal = (p<ema)*(-1) #-1 for holding a short position
#         signal.iloc[:,-1]=0 #always close position at the market close
    
#         for i in range(period+1, p.shape[0]):
#             for j in range(p.shape[1]):
#             # check if the position is open
#                 if signal.iloc[i-1,j] != 0:
#                 # check if the price has dropped by more than 7%
#                     if (p.iloc[i,j] / p.iloc[i-period-1,j]) < 0.83:
#                         signal.iloc[i,j] = 0 # close the position
#                 # check if the last 3 SMA values have been decreasing
#                 elif (ema.iloc[i-1,j] < ema.iloc[i-2,j]) and (ema.iloc[i-2,j] < ema.iloc[i-3,j]):
#                     signal.iloc[i,j] = 0 # close the position
        

#         return ema, signal


# def EMA(p, period=3, signal_type='long'):
#     # p - price used for EMA, the nxm DataFrame
#     # period - look-back period size for EMA calculation
#     # signal_type - long (default), short, or both (not recommended)
#     signal = pd.DataFrame(index=p.index,columns=p.columns)
#     emaTen = pd.DataFrame(index=p.index,columns=p.columns)
#     emaFive = pd.DataFrame(index=p.index,columns=p.columns)        
#     for idx in p.index:
#         ema_valTen = p.loc[idx].ewm(span=10, min_periods=period).mean()
#         emaTen.loc[idx] = ema_valTen
#         ema_valFive = p.loc[idx].ewm(span=5, min_periods=period).mean()
#         emaFive.loc[idx] = ema_valFive
#         if signal_type=='long':
#             signal = (ema_valTen>ema_valFive) & (p>emaTen)*1 #1 for holding a long position
#         elif signal_type=='short':
#             signal = (ema_valTen<ema_valFive) & (p<emaTen)*(-1) #-1 for holding a short position
#             signal.iloc[:,-1]=0 #always close position at the market close
#           return emaTen, emaFive, signal

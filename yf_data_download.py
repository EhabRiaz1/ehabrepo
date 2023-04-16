# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 08:59:07 2023
@author: pastor&benji
"""
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt

def merge_data(file1,file2):
    #read file1 and file2 as dataframe; merge to df
    #to extend historical data records
    date_parser = lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S')
    df1 = pd.read_csv(file1, parse_dates=['Datetime'], date_parser=date_parser, index_col='Datetime')
    df2 = pd.read_csv(file2, parse_dates=['Datetime'], date_parser=date_parser, index_col='Datetime')
    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    ind = np.sum(np.isnan(df.iloc[:,:6]),axis=1).values==6
    df.iloc[ind,:6] = df.iloc[ind,6:]
    df = df.iloc[:,:6]
    df.columns=df1.columns
    
    return df


# #take a look at the data types
# type(df.index)
# df.dtypes
# print(df[0:5])

# ''' download and merge your data'''
# df = yf.download(tickers='AMZN', start=datetime(2023,4,3), end=datetime(2023,4,10), interval="1m")
# df.to_csv('AMZN_1m_1.csv') 
# df2 = yf.download(tickers='AMZN', start=datetime(2023,3,26), end=datetime(2023,4,2), interval="1m")
# df2.to_csv('AMZN_1m_2.csv')
# df3 = yf.download(tickers='AMZN', start=datetime(2023,3,18), end=datetime(2023,3,25), interval="1m")
# df3.to_csv('AMZN_1m_3.csv')
# df4 = yf.download(tickers='AMZN', start=datetime(2023,3,13), end=datetime(2023,3,17), interval="1m")
# df4.to_csv('AMZN_1m_4.csv')


df = yf.download(tickers='AMZN', start=datetime(2023,4,5), end=datetime(2023,4,11), interval="1m").resample('1T').ffill().head(1950)
df.to_csv('AMZN_1m_1.csv') 
df2 = yf.download(tickers='AMZN', start=datetime(2023,3,30), end=datetime(2023,4,5), interval="1m").resample('1T').ffill().head(1950)
df2.to_csv('AMZN_1m_2.csv')
df3 = yf.download(tickers='AMZN', start=datetime(2023,3,22), end=datetime(2023,3,29), interval="1m").resample('1T').ffill().head(1950)
df3.to_csv('AMZN_1m_3.csv')
df4 = yf.download(tickers='AMZN', start=datetime(2023,3,17), end=datetime(2023,3,21), interval="1m").resample('1T').ffill().head(1950)
df4.to_csv('AMZN_1m_4.csv')





#merge the two dataset
df_12 = merge_data('AMZN_1m_1.csv','AMZN_1m_2.csv')
df_12.to_csv('first_merge.csv')
df_22 = merge_data('AMZN_1m_3.csv','AMZN_1m_4.csv')
df_22.to_csv('second_merge.csv')
month_df = merge_data('first_merge.csv','second_merge.csv')
month_df.to_csv('Amzn_13-11_March-April')



# Plot the close price of the AAPL
month_df['Adj Close'].plot()
plt.show()





    
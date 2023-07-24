###############################################################################
###############################################################################
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt

import os
os.getcwd() #know your work directory
# os.chdir('./') #set your work directory, e.g. C:/Users/c0000000
os.chdir('/Users/ehabriaz/Desktop/pytonbacktest')

###############################################################################
###############################################################################
###############################################################################
###############################################################################


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

###############################################################################
###############################################################################


###############################################################################
###############################################################################
tickerSymbol = 'AMZN'
start_date = datetime(2023, 4, 17) ###########MODIFY PER DAY
end_date = datetime(2023, 5, 15)  ###########MODIFY PER DAY
interval = "1m"
###############################################################################
###############################################################################

###############################################################################
###############################################################################
delta = timedelta(days=7)
count = 1

while start_date < end_date:
    # Download data for a 7-day period
    temp_end_date = min(start_date + delta, end_date)
    df = yf.download(tickers=tickerSymbol, start=start_date, end=temp_end_date, interval=interval)
    # df = df.resample('1T').ffill().head(1950)
    
    
    # Save the data to a CSV file
    tickerDataSTR = f"AMZN_1m_{count}.csv"
    df.to_csv(tickerDataSTR)
    
    # Update start date and count
    start_date += delta
    count += 1
###############################################################################
###############################################################################

###############################################################################
###############################################################################
df1 = pd.read_csv('AMZN_1m_1.csv', index_col='Datetime', parse_dates=['Datetime'])
df2 = pd.read_csv('AMZN_1m_2.csv', index_col='Datetime', parse_dates=['Datetime'])
df3 = pd.read_csv('AMZN_1m_3.csv', index_col='Datetime', parse_dates=['Datetime'])
df4 = pd.read_csv('AMZN_1m_4.csv', index_col='Datetime', parse_dates=['Datetime'])

df_12 = merge_data('AMZN_1m_1.csv','AMZN_1m_2.csv')
df_12.to_csv('first_merge.csv')

df_22 = merge_data('AMZN_1m_3.csv','AMZN_1m_4.csv')
df_22.to_csv('second_merge.csv')

month_df = merge_data('first_merge.csv','second_merge.csv')
month_df.to_csv('Amzn_13-11_lastMonth.csv')
###############################################################################
###############################################################################

###############################################################################
###############################################################################
###############################################################################
###############################################################################

# Plot the close price of the AAPL
month_df['Adj Close'].plot()
plt.show()





    

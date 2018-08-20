
import plotly as pl
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as web
from datetime import datetime

def resample_to_timeframe(daily_df,tf='d'):
    if tf is not 'd':
        resampled_df = daily_df.copy()
        resampled_df['Date'] = pd.to_datetime(resampled_df['Date'])
        resampled_df.set_index('Date',inplace=True)
        resampled_df.sort_index(inplace=True)
        # resample, with date in index
        if tf is 'm':
            resample_value = '1M'
        elif tf is 'w':
            resample_value = 'W'
        else :
            resample_value = '3M'
        print("Resampling data to ",resample_value)    
        resampled_df = resampled_df.resample(resample_value).agg({'Open':'first','High': 'max', 'Low': 'min', 'Close': 'last'})
        return resampled_df
    else:
        return daily_df

pd.options.mode.chained_assignment = None

def calculate_returns_col(dataframe):
    df_with_returns = dataframe[['Open','Close','High','Low']]
    # returns calculation in percentage: (close-open)/open
    df_with_returns['Returns'] = pd.Series(100*(dataframe['Close'] - dataframe['Open'])/dataframe['Open'],index=df_with_returns.index)
    df_with_returns.sort_values(['Returns'],ascending=[1])
    return df_with_returns

# unused
def generate_intervals(min_val,max_val):
    mid = min(int((abs(min_val) + abs(max_val)) / 2),5)
    intervals_1 = [x for x in range(-min_val,0,1)]
    intervals_2 = [x for x in range(0,max_val,1)]
    intervals = intervals_1 + intervals_2
    #intervals = [int(x) for x in np.linspace(min_val,max_val,mid)]
    return intervals

def calculate_freq_table(df_trans):
    intervals = [-4,-3,-2,-1,0,1,2,3,4]
    freq_table = pd.crosstab(np.digitize(df_trans['Returns'],intervals),'frequencies', colnames=['intervals'])
    
    if len(freq_table) >= 2:
        index_list = [str(intervals[i]) + ' to ' + str(intervals[i+1]) for i in range(len(freq_table)-2)]
        index_list.insert(0, 'less than ' + str(intervals[0]))
        index_list.append('greater than ' + str(intervals[len(intervals)-1]))
    else:
        index_list = []
        index_list.insert(0, 'less than ' + str(intervals[0]))
        index_list.append('greater than '+ str(intervals[len(intervals)-1]))
    
    freq_table.index = pd.Index(index_list)
    return (index_list,freq_table)

def plot_distribution(index_list, freq_table):
    indexes = index_list
    frequencies = [x for x in freq_table['frequencies']]
    pos = np.arange(len(indexes))
    width = 1.0
    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(indexes)
    plt.bar(pos, frequencies, width, color='b',edgecolor = "black")
    
    for item in ax.get_xticklabels():
        item.set_rotation(45)
    #plt.show()
    plt.savefig('distrib.png')


def main():
    pl.tools.set_credentials_file(username='dafe52', api_key='Elsx2TmghmZZHHvSZBjl')

    # Parameters
    symbol = "DIS"
    csv_file_path = './DIS.csv' # daily

    df = pd.read_csv(csv_file_path)
    df = df.drop(columns=['Volume'])
    print("Data read to Pandas dataframe from file ",csv_file_path)

    #df = to_quarterly(df)
    df = resample_to_timeframe(df, 'w')
    df_returns = calculate_returns_col(df)
    (i_list,freq) = calculate_freq_table(df_returns)
    plot_distribution(i_list,freq)

    all_sum = freq.sum()
    freq['probability'] = 100 * freq['frequencies'] / all_sum['frequencies']
    freq['cumulative_probability'] = freq['probability'].cumsum()
    print(freq)   

main()
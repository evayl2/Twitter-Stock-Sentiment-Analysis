import requests
import json
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

def plot_multiple_stocks():
    API_URL = "https://www.alphavantage.co/query"
    data = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "GME",
        "outputsize": "compact",
        "datatype": "json",
        "apikey": "J5S1HUA0WPM10KU8"}
    response = requests.get(API_URL, data)
    response_json = response.json()
    ts = TimeSeries(key='J5S1HUA0WPM10KU8', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='GME',interval='60min', outputsize='compact')
    df1 = data['4. close']
    print(df1)
    data2 = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "TSLA",
        "outputsize": "compact",
        "datatype": "json",
        "apikey": "J5S1HUA0WPM10KU8"}
    response2 = requests.get(API_URL, data2)
    response_json2 = response2.json()
    ts2 = TimeSeries(key='J5S1HUA0WPM10KU8', output_format='pandas')
    data2, meta_data2 = ts2.get_intraday(symbol='TSLA',interval='60min', outputsize='compact')
    df2 = data2['4. close']
    print(df2)
    total_df = pd.concat([df1,df2], axis=1)
    total_df.plot()
    plt.title('Intraday Times Series for GME vs TESLA stock')
    plt.ylabel('Cost (dollars)')
    plt.xlabel('Time')
    plt.legend((df1,df2),('GME','TSLA'))
    plt.show()

def plot_single_stock():
    print("Enter stock name to search for")
    symbol = input()
    API_URL = "https://www.alphavantage.co/query"
    data = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "datatype": "json",
        "apikey": "J5S1HUA0WPM10KU8"}
    response = requests.get(API_URL, data)
    response_json = response.json()
    ts = TimeSeries(key='J5S1HUA0WPM10KU8', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='compact')
    df1 = data['4. close']
    return df1, symbol
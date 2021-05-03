import requests
import json
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

def plot_single_stock():
    symbol = "GOOGL"
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
    data, meta_data = ts.get_intraday(symbol=symbol, outputsize='compact')
    data = data.reset_index()

    return data, symbol


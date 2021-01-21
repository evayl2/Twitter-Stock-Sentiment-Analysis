import requests
import json
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas

API_URL = "https://www.alphavantage.co/query"
data = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "COST",
    "outputsize": "compact",
    "datatype": "json",
    "apikey": "J5S1HUA0WPM10KU8"}
response = requests.get(API_URL, data)
response_json = response.json()
print(type(response_json))
ts = TimeSeries(key='J5S1HUA0WPM10KU8', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='COST',interval='15min', outputsize='full')
data['4. close'].plot()
plt.title('Intraday Times Series for the COSTCO stock (1 min)')
plt.show()



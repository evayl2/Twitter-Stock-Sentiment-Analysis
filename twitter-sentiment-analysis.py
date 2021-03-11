from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import string
import nltk
from stockjson import *

cleaned_tweets = pd.read_csv(r"tweet_data\cleaned_user_tweet.csv")
vader = SentimentIntensityAnalyzer()
tweet_sentiment = pd.DataFrame()
tweet_sentiment['tweet'] = cleaned_tweets['text']
scores = cleaned_tweets['text'].apply(vader.polarity_scores).tolist()
scores_df = pd.DataFrame(scores)
# print(scores_df['neu'])
tweet_sentiment["neg"] = scores_df["neg"]
tweet_sentiment['neu'] = scores_df['neu']
tweet_sentiment["pos"] = scores_df["pos"]
tweet_sentiment["compound"] = scores_df["compound"]
tweet_sentiment["time"] = cleaned_tweets['date'].astype('datetime64[ns]')
tweet_sentiment.to_csv(index=False, path_or_buf="tweet_data/user_tweet_sentiment.csv")

stock_prices = pd.read_csv('google_stocks.csv')
# stock_date = []
# for date in (stock_prices['date'].values.tolist()):
#     stock_date += [str(date).split(" ")[0]]
# stock_prices['day'] = pd.DataFrame(stock_date)
stock_name = 'GOOGL'
# tweet_sentiment.plot(tweet_sentiment['time'], tweet_sentiment['compound'], color='r')
# stock_plot = stock_prices.plot(stock_prices['date'], stock_prices['4. close'])
# # stock_plt1 = stock_plot.twinx()
#

# print(tweet_sentiment['time'])
tweet_sentiment.plot('time','compound')
plt.title('Intraday Times Series for ' + stock_name + ' vs #Google tweet sentiment')
plt.ylabel('Cost (dollars)')
plt.xlabel('Time')

plt.show()

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
tweet_sentiment["time"] = cleaned_tweets['date']
tweet_sentiment.to_csv(index=False, path_or_buf="tweet_data/user_tweet_sentiment.csv")

stock_prices, stock_name = plot_single_stock()
print(stock_prices)
stock_plot = stock_prices.plot()
stock_plt1 = stock_plot.twinx()
stock_prices.plot(tweet_sentiment['time'], tweet_sentiment['compound'], ax=stock_plt1, color='r')
plt.title('Intraday Times Series for' + stock_name + 'vs Elon Musk Tweet Sentiment')
plt.ylabel('Cost (dollars)')
plt.xlabel('Time')

plt.show()
# def visualize_tweet_stock():

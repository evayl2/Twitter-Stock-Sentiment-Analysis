from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import string
import nltk
from stockjson import *
import datetime

# RUN EVERY DAY
# CHANGE DATETIME CONSTANTS IN Weigh_Tweets() AND Parse_Stock_Prices()
def Weigh_Tweets(clean_tweets):
    seven_day_sentiment = pd.read_csv("weighed_tweet_scores.csv")
    seven_day_sentiment.drop(seven_day_sentiment.columns[[0]], axis=1, inplace=True)
    weighed_tweet_scores = pd.DataFrame(columns=['Date','Average Sentiment'])
    morning_total_followers = 0
    afternoon_total_followers = 0
    current = datetime.datetime.now()
    time1 = datetime.time(12, 5, 0)
    times = clean_tweets['time'].dt.time.tolist()
    followers = clean_tweets['follower_count'].values.tolist()
    compound_scores = clean_tweets['compound'].values.tolist()
    for i in range(len(times)):
        if times[i] < time1:
            morning_total_followers += followers[i]
        else:
            afternoon_total_followers += followers[i]
    total_morning_sentiment = 0
    total_afternoon_sentiment = 0
    for i in range(len(times)):
        if times[i] < time1:
            total_morning_sentiment += compound_scores[i]*followers[i]
        else:
            total_afternoon_sentiment += compound_scores[i]*followers[i]
    today = pd.DataFrame()
    if morning_total_followers == 0:
        total_morning_sentiment = 0
        total_afternoon_sentiment /= afternoon_total_followers
        today = pd.DataFrame([[afternoon_today, total_afternoon_sentiment]],
                             columns=['Date', 'Average Sentiment'])
    elif afternoon_total_followers == 0:
        total_afternoon_sentiment = 0
        total_morning_sentiment /= morning_total_followers
        today = pd.DataFrame([[morning_today, total_morning_sentiment]],
                             columns=['Date','Average Sentiment'])
    else:
        total_afternoon_sentiment /= afternoon_total_followers
        total_morning_sentiment /= morning_total_followers
        today = pd.DataFrame([[morning_today, total_morning_sentiment],[afternoon_today, total_afternoon_sentiment]],
                             columns=['Date', 'Average Sentiment'])
    weighed_tweet_scores = weighed_tweet_scores.append(today)
    seven_day_sentiment = seven_day_sentiment.append(weighed_tweet_scores)
    seven_day_sentiment.to_csv('weighed_tweet_scores.csv')
    return seven_day_sentiment

def Parse_Stock_Prices(stock_prices):
    seven_day_prices = pd.read_csv("seven_day_prices.csv")
    seven_day_prices.drop(seven_day_prices.columns[[0]], axis=1, inplace=True)
    time1 = datetime.time(12, 0, 0)
    times = stock_prices['date'].dt.time.tolist()
    prices = stock_prices['4. close'].values.tolist()
    morning_count = 0
    afternoon_count = 0
    for i in range(len(times)):
        if times[i] < time1:
            morning_count += 1
        else:
            afternoon_count += 1
    morning_price = 0
    afternoon_price = 0

    for i in range(len(times)):
        if times[i] < time1:
            morning_price += prices[i]
        else:
            afternoon_price += prices[i]
    morning_price /= morning_count
    afternoon_price /= afternoon_count
    average_prices = pd.DataFrame(columns=['date', 'Average Stock Price'])

    # CHANGE EVERY TIME YOU RUN TO CURRENT DATE
    morning = datetime.datetime.now()
    morning_today = morning.replace(hour=0, minute=0)
    afternoon_today = morning.replace(hour=12, minute=0)
    today = pd.DataFrame([[morning_today, morning_price], [afternoon_today, afternoon_price]],
                         columns=['date', 'Average Stock Price'])
    average_prices = average_prices.append(today, ignore_index = True)
    seven_day_prices = seven_day_prices.append(average_prices)
    seven_day_prices.to_csv('seven_day_prices.csv')
    return seven_day_prices


cleaned_tweets = pd.read_csv(r"tweet_data\cleaned_hashtag_tweet.csv")
vader = SentimentIntensityAnalyzer()
tweet_sentiment = pd.DataFrame()
tweet_sentiment['tweet'] = cleaned_tweets['text']
scores = cleaned_tweets['text'].apply(vader.polarity_scores).tolist()
scores_df = pd.DataFrame(scores)
# print(scores_df['neu'])
tweet_sentiment["follower_count"] = cleaned_tweets["follower_count"]
tweet_sentiment["neg"] = scores_df["neg"]
tweet_sentiment['neu'] = scores_df['neu']
tweet_sentiment["pos"] = scores_df["pos"]
tweet_sentiment["compound"] = scores_df["compound"]
tweet_sentiment["time"] = cleaned_tweets['date'].values.astype('datetime64[ns]')
tweet_sentiment.to_csv(index=False, path_or_buf="tweet_data/hashtag_tweet_sentiment.csv")
weighed_tweets = Weigh_Tweets(tweet_sentiment)
# weighed_tweets = pd.read_csv('weighed_tweet_scores.csv')
times2 = pd.to_datetime(weighed_tweets['Date'], errors='coerce')
print(times2)

stock_prices, symbol = plot_single_stock()
stock_prices.to_csv("google_stocks.csv")
# print(stock_prices.columns.values.tolist())
# stock_prices = pd.read_csv('google_stocks.csv')

stock_prices['date'] = (stock_prices['date']).values.astype(dtype='datetime64[ms]')
stock_prices = Parse_Stock_Prices(stock_prices)
stock_prices = pd.read_csv('seven_day_prices.csv')
stock_prices.drop(stock_prices.columns[[0]], axis=1, inplace=True)
stock_prices.to_csv('seven_day_prices.csv')
times = pd.to_datetime(stock_prices['date'], errors='coerce')
# print(stock_prices
stock_name = 'GOOGL'
fig,ax = plt.subplots()
# # make a plot
ax.plot(times, stock_prices['Average Stock Price'], color="red", marker="o")
# set x-axis label
ax.set_xlabel("date",fontsize=14)
# set y-axis label
ax.set_ylabel("stock price", color="red",fontsize=14)

ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(times2, weighed_tweets["Average Sentiment"],color="blue",marker="o")
ax2.set_ylabel("Average Sentiment", color="blue", fontsize=14)
plt.show()
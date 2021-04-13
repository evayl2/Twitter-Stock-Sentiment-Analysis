import requests
from twitterconfig import *
import pandas as pd
import tweepy
import re
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import string
import nltk
from nltk.stem.porter import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from wordcloud import WordCloud


## RUN EVERY DAY
# Store tweets data in a dataframe
def tweets_df(results):
    # saved_tweets = pd.read_csv("tweet_data/seven_day_tweets.csv")
    # id_list = [tweet.id for tweet in results]
    # data_set = pd.DataFrame(id_list, columns=["id"])
    # data_set["text"] = [tweet.text for tweet in results]
    # data_set["Hashtags"] = [tweet.entities['hashtags'] for tweet in results]
    # data_set["date"] = [tweet.created_at for tweet in results]
    # data_set["follower_count"] = [tweet.user.followers_count for tweet in results]
    # saved_tweets = saved_tweets.append(data_set)
    # filename = "tweet_data/hashtag_scraped_tweets.csv"
    # saved_tweets.to_csv(filename)
    # return saved_tweets

    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])
    data_set["text"] = [tweet.text for tweet in results]
    data_set["Hashtags"] = [tweet.entities['hashtags'] for tweet in results]
    data_set["date"] = [tweet.created_at for tweet in results]
    data_set["follower_count"] = [tweet.user.followers_count for tweet in results]
    # saved_tweets = saved_tweets.append(data_set)
    filename = "tweet_data/seven_day_tweets.csv"
    data_set.to_csv(filename)
    return data_set

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(twitter["API_KEY"], twitter["API_KEY_SECRET"])  # Interacting with twitter's API
    auth.set_access_token(twitter["ACCESS_TOKEN"], twitter["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth, wait_on_rate_limit=True)  # creating the API object

    # print("Enter Twitter HashTag to search for")
    words = "#google"

    # Extracting Tweets
    results = []
    for tweet in tweepy.Cursor(api.search, q=words, lang='en').items(1000):
        results.append(tweet)

    data_set = tweets_df(results)


def get_tweets_from_user(results):
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])
    data_set["text"] = [tweet.text for tweet in results]
    data_set["User"] = [tweet.user.screen_name for tweet in results]
    data_set["date"] = [tweet.created_at for tweet in results]


    filename = 'tweet_data/scraped_user_tweets.csv'
    # we will save our database as a CSV file.
    data_set.to_csv(filename)
    return data_set


# if __name__ == '__main__':
#     # pass in the username of the account you want to download
#     auth = tweepy.OAuthHandler(twitter["API_KEY"], twitter["API_KEY_SECRET"])  # Interacting with twitter's API
#     auth.set_access_token(twitter["ACCESS_TOKEN"], twitter["ACCESS_TOKEN_SECRET"])
#     api = tweepy.API(auth, wait_on_rate_limit=True)  # creating the API object
#
#     print("Enter Twitter username to search for")
#     words = input()
#
#     results = []
#     for tweet in tweepy.Cursor(api.user_timeline,id=words).items(50):
#         results.append(tweet)
#
#     data_set = get_tweets_from_user(results)


# Tweet parsing code from https://www.analyticsvidhya.com/blog/2018/07/hands-on-sentiment-analysis-dataset-python/

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt

data = pd.read_csv('tweet_data/seven_day_tweets.csv')
urls = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
data["text"] = np.vectorize(remove_pattern)(data['text'], urls)
data["text"] = np.vectorize(remove_pattern)(data['text'], "@[\w]*")
data["text"] = data['text'].str.replace("[^a-zA-Z#]", " ")
data["text"] = data["text"].apply(lambda x: ' '.join([w for w in x.split() if len(w)>2]))

nan_value = float("NaN")
data.replace("", nan_value, inplace=True)
data.dropna(subset = ["text"], inplace=True)

data.to_csv(index=False, path_or_buf="tweet_data/cleaned_hashtag_tweet.csv")


import requests
from twitterconfig import *
import pandas as pd
import tweepy



# # Store tweets data in a dataframe
# def tweets_df(results):
#     id_list = [tweet.id for tweet in results]
#     data_set = pd.DataFrame(id_list, columns=["id"])
#     data_set["text"] = [tweet.text for tweet in results]
#     data_set["Hashtags"] = [tweet.entities.get('hashtags') for tweet in results]
#
#     filename = 'scraped_tweets.csv'
#     # we will save our database as a CSV file.
#     data_set.to_csv(filename)
#     return data_set
#
#
# if __name__ == '__main__':
#
#     auth = tweepy.OAuthHandler(twitter["API_KEY"], twitter["API_KEY_SECRET"])  # Interacting with twitter's API
#     auth.set_access_token(twitter["ACCESS_TOKEN"], twitter["ACCESS_TOKEN_SECRET"])
#     api = tweepy.API(auth, wait_on_rate_limit=True)  # creating the API object
#
#     # Enter Hashtag and initial date
#     print("Enter Twitter HashTag to search for")
#     words = input()
#
#     # Extracting Tweets
#     results = []
#     for tweet in tweepy.Cursor(api.search, q=words, lang="en").items(5):
#         results.append(tweet)
#
#     data_set = tweets_df(results)
#

def get_tweets_from_user(results):
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])
    data_set["text"] = [tweet.text for tweet in results]
    data_set["User"] = [tweet.user.screen_name for tweet in results]


    filename = 'scraped_user_tweets.csv'
    # we will save our database as a CSV file.
    data_set.to_csv(filename)
    return data_set


if __name__ == '__main__':
    # pass in the username of the account you want to download
    auth = tweepy.OAuthHandler(twitter["API_KEY"], twitter["API_KEY_SECRET"])  # Interacting with twitter's API
    auth.set_access_token(twitter["ACCESS_TOKEN"], twitter["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth, wait_on_rate_limit=True)  # creating the API object

    print("Enter Twitter username to search for")
    words = input()

    results = []
    for tweet in tweepy.Cursor(api.user_timeline,id=words).items(5):
        results.append(tweet)

    data_set = get_tweets_from_user(results)
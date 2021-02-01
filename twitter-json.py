import requests
import twitterconfig
response = requests.get(
    'https://api.twitter.com/1.1/search/tweets.json?q=tesla',
    headers={
        'authorization': 'Bearer '+twitterconfig.twitter["BEARER_TOKEN"]
})
print(response.json())
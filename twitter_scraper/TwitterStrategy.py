import os
import pandas as pd
from Utils.TwitterUtils import *
from utils import loadFromPickle, saveAsPickle


# keys
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# authorization
api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)

# search tweets
search_words = "$MSFT"
date_since = "2021-11-10"
item_num = 100
#tweet_list = search_keywords(api, search_words, date_since, item_num)
#for tweet in tweet_list:
#    print(tweet)


# search user
screen_name = ""
user_info = search_user_info(api, screen_name)
#for key in user_info.keys():
#    print(key + " : " + str(user_info[key]))


# get list of people following
friends_screen_name = get_friends(api, screen_name)

# search all tweets from friends
date = "2021-11-12"
total_tweets = []
for screen_name in friends_screen_name:
    print(screen_name)
    tweets = search_tweets_by_username(api, screen_name, date)
    total_tweets.append(tweets)

# save as pickle
saveAsPickle(total_tweets, 'tweets_'+date+'.pkl')


# write to csv
columns = ["name", "date", "ticker", "content"]
total_list = loadFromPickle('tweets_'+date+'.pkl')
write_tweets_to_csv("tweets_"+date+".csv", columns, total_list)

import os
import pandas as pd
from Utils.TwitterUtils import *
from utils import loadFromPickle, saveAsPickle


# keys
consumer_key = "SKd3b9Cfp8xjFadQTCTnmcyfR"
consumer_secret = "m7fMMC5qMkhFfrCWKhyEOAMxv4hAqI3U6CWhZya7i8G7A78vbB"
access_token = "2741104517-jlbKcK39Bt8ZJwKCkreJtSxVpc85lxhVoBPenlm"
access_token_secret = "dvAhD1Z7Wquuy2dWd6YrAPU9lwFaRehLbDud0ExSq1K43"

# authorization
api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)

# search tweets
search_words = "$CHWY"
date_since = "2020-12-10"
item_num = 100
#tweet_list = search_keywords(api, search_words, date_since, item_num)
#for tweet in tweet_list:
#    print(tweet)


# search user
user_name = "Alex94085223"
#user_info = search_user_info(api, user_name)
#for key in user_info.keys():
#    print(key + " : " + str(user_info[key]))

# search friends
user = api.get_user("Alex94085223")
friends_screen_name = []
for friend in user.friends():
    friends_screen_name.append(friend.screen_name)


# search all tweets from friends
date = "2021-03-31"
total_tweets = []
skip_list = ["MrZackMorris", "ripster47"]
for screen_name in friends_screen_name:
    print(screen_name)
    # error: cannot read this guys twitter since 02/25
    if screen_name not in skip_list:
        tweets = search_tweets_by_username(api, screen_name, date)
        total_tweets.append(tweets)

# save as pickle
saveAsPickle(total_tweets, 'tweets_'+date+'.pkl')


# write to csv
columns = ["name", "date", "ticker", "content"]
total_list = loadFromPickle('tweets_'+date+'.pkl')
write_tweets_to_csv("tweets_"+date+".csv", columns, total_list)
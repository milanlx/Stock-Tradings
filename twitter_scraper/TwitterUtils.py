import tweepy as tw
import re
import datetime
import csv


def get_api(consumer_key, consumer_secret, access_token, access_token_secret):
    """ call the API
    """
    # authorization of consumer key and consumer secret
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    # set access to user's access key and access secret
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    return api


def search_user_info(api, screen_name):
    """ return dictionary containing:
         - screen name, name (on display), description, num of follower, num of friends
    """
    user_info = {}
    user = api.get_user(screen_name)
    user_info["screen_name"] = str(user.screen_name)
    user_info["name"] = str(user.name)
    user_info["description"] = str(user.description)
    user_info["num_of_followers"] = int(user.followers_count)
    user_info["num_of_friends"] = int(user.friends_count)
    return user_info


def search_tweets_by_keywords(api, search_words, date_since, item_num):
    """ search tweets by key words, return as a list
    """
    tweet_list = []
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       tweet_mode="extended",
                       since=date_since).items(item_num)
    for tweet in tweets:
        if "retweeted_status" in dir(tweets):
            tweet_list.append(tweet.retweeted_status.full_text)
        else:
            tweet_list.append(tweet.full_text)
    return tweet_list


# TODOLIST: remove retweets
def search_tweets_by_username(api, screen_name, date):
    """ search tweets by user name and during start and end date ("YYYY-MM-DD")
        return a list of dict with keys:
            - name, date, stock ticker, content
    """
    tweet_list = []
    # get name (on display)
    user_info = search_user_info(api, screen_name)
    name = user_info["name"]
    year, month, day = date.split('-')
    start_date = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
    end_date = datetime.datetime(int(year), int(month), int(day), 23, 59, 59)

    tweets = []
    tmpTweets = api.user_timeline(screen_name)
    for tweet in tmpTweets:
        if tweet.created_at < end_date and tweet.created_at > start_date:
            tweets.append(tweet)
    while (tmpTweets[-1].created_at > start_date):
        tmpTweets = api.user_timeline(screen_name, max_id=tmpTweets[-1].id)
        for tweet in tmpTweets:
            if tweet.created_at < end_date and tweet.created_at > start_date:
                tweets.append(tweet)

    # filter
    for tweet in tweets:
        text = str(tweet.text).strip()
        # remove emoji
        text = remove_emoji(text)
        words = text.strip().split(' ')
        # find stock tickers
        tickers = [ticker for ticker in words if "$" in ticker and not bool(re.search(r'\d', ticker))
                   and ticker != "$…"]
        tickers_set = set(tickers)
        if len(tickers_set) > 0:
            for ticker in tickers_set:
                # filter non-tickers
                if 0 < len(ticker) < 6:
                    # filter retweets
                    if text[0:4] != "RT @":
                        tweet_dict = {"name": name,
                                      "date": date,
                                      "ticker": re.sub('[^a-zA-Z]+', '', ticker).upper(),
                                      "content": text}
                        tweet_list.append(tweet_dict)
    return tweet_list


def get_friends(api, screen_name):
    """ search people following given screen_name, return as a list
    """
    friends_screen_name = []
    friends = api.friends(screen_name)
    for friend in friends:
        friends_screen_name.append(friend.screen_name)
    return friends_screen_name



def remove_emoji(text):
    """
    remove emoji symbols from tweet
    """
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    return RE_EMOJI.sub(r'', text)


def write_tweets_to_csv(file_path, header_line, total_list):
    """ write to csv file
    """
    with open(file_path, encoding="utf-8", mode="w", newline="") as csv_file:
        # header line
        writer = csv.DictWriter(csv_file, fieldnames=header_line)
        writer.writeheader()
        for tweet_list in total_list:
            for tweet in tweet_list:
                writer.writerow(tweet)
    return 0

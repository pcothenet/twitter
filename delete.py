import os
import tweepy
import time
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_key = os.environ.get("TWITTER_ACCESS_TOKEN")
access_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print("Authenticated as: %s - %s" %(api.me().screen_name,api.me().id))

def show_last_tweets():
    public_tweets = api.user_timeline(api.me().id, count=1)
    for tweet in public_tweets:
        print(tweet.id)
        print(tweet.text)

def delete_last_tweets(count):
    public_tweets = api.user_timeline(api.me().id, count=count, max_id=883052332270755842)
    for tweet in public_tweets:
        print(tweet)
        if tweet.retweeted == True:
            api.destroy_status(tweet.id)

def delete_old_tweets():
    for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=api.me().id, count=100, max_id=883052332270755842).items()):
        delete = False
        if (tweet.retweeted == True) or (tweet.text[0:2] == 'RT'):
            delete = True
        elif 't.co' in tweet.text:
            delete = True
        elif (tweet.in_reply_to_user_id != None) or (tweet.in_reply_to_status_id != None): 
            delete = True
        if delete:
            print(tweet.text, 'delete')
            api.destroy_status(tweet.id)

# rate_limit = api.rate_limit_status()
# print(rate_limit)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


# delete_last_tweets(count=1)
delete_old_tweets()
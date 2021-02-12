import os
import tweepy
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_key = os.environ.get("TWITTER_ACCESS_TOKEN")
access_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print("Authenticated as: %s - %s" %(api.me().screen_name,api.me().id))

PROTECTED_TWEETS = [
    528708940507254786,
    883052332270755842,
    775167109357711360,
    770997971269787648,
    637976082277339137,
    635148852862033920,
    1360280315197968389,
    1360281198363176962
]

def show_last_tweets():
    public_tweets = api.user_timeline(api.me().id, count=1)
    for tweet in public_tweets:
        print(tweet.id)
        print(tweet.text)

def limit_handled(cursor):
    print(cursor)
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

def delete_old_tweets():
    # for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id=api.me().id, count=100).items()):
    for tweet in tweepy.Cursor(api.user_timeline, id=api.me().id, count=100).items():
        delete = False
        if tweet.id in PROTECTED_TWEETS:
            print(tweet.id, 'protected')
            delete = False
        elif (tweet.created_at < datetime.today() - timedelta(days=14)):
            delete = True
        # elif (tweet.retweeted == True) or (tweet.text[0:2] == 'RT'):
        #     delete = True
        # elif 't.co' in tweet.text:
        #     delete = True
        # elif (tweet.in_reply_to_user_id != None) or (tweet.in_reply_to_status_id != None): 
        #     delete = True
        if delete:
            print(tweet.text, tweet.created_at, 'delete')
            api.destroy_status(tweet.id)


# delete_old_tweets()

def handler(event, context):
    delete_old_tweets()
    return {
        'message': 'The function executed successfully!',
        'event': event
    }
import os
import tweepy
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_key = os.environ.get("TWITTER_ACCESS_TOKEN")
access_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

def oauth_login():
    """Authenticate with twitter using OAuth"""
    print(consumer_key, access_key)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    print("Authenticated as: %s" % api.me().screen_name)

oauth_login()
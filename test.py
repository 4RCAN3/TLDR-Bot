import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('API_KEY')
API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get('BEARER')

client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)

tweet = client.get_tweet('1550960310412001281', tweet_fields = ['referenced_tweets'])

print(tweet.data['referenced_tweets'][-1].id)
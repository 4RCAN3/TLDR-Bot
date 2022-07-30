#importing libraries

try:
    import tweepy
    from dotenv import load_dotenv
    import os
    import time
except Exception as e:
    print('Import error', e)


load_dotenv()
BEARER_TOKEN = os.environ.get('BEARER')

class Stream(tweepy.StreamingClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        """__init__( \
            bearer_token, *, return_type=Response, wait_on_rate_limit=False, \
            chunk_size=512, daemon=False, max_retries=inf, proxy=None, \
            verify=True \
        )
        """

        API_KEY = os.environ.get('API_KEY')
        API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
        ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
        ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

        self.client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)
        auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def on_connect(self):
        print('Stream started')
    
    def _get_thread(self, tweet):
        repliedTo = tweet.data['referenced_tweets'][0]['id']
        thread = []

        while repliedTo != None:
            repliedTo = self.client.get_tweet(repliedTo, tweet_fields = ['referenced_tweets'])
            thread.append(repliedTo.data['text'])
            repliedTo = repliedTo.data['referenced_tweets'][-1].id if repliedTo.data['referenced_tweets'] != None and repliedTo.data['referenced_tweets'][-1].type == 'replied_to' else None    
        
        thread = '\n'.join(thread[::-1])

        return thread

    def on_tweet(self, tweet):
        print('Fetching thread')
        thread = self._get_thread(tweet)
        print(thread)
        time.sleep(0.2)
        pass

rules = ['@Arcane45882959 is:reply']

stream = Stream(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

for rule in rules:
    stream.add_rules(tweepy.StreamRule(rule))

stream.filter(tweet_fields = ['conversation_id', 'referenced_tweets'])
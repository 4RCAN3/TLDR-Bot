#importing libraries

try:
    import tweepy
    from dotenv import load_dotenv
    import os
    import time
    import generate
except Exception as e:
    print('Import error', e)


load_dotenv()
BEARER_TOKEN = rf"{os.environ.get('BEARER')}"

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
    
    def _get_thread(self, tweet) -> str:
        repliedTo = tweet.data['referenced_tweets'][0]['id']
        thread = []
        intro = ''
        while repliedTo != None:
            repliedTo = self.client.get_tweet(repliedTo, tweet_fields = ['referenced_tweets'], user_fields = ['name', 'username'], expansions = ['author_id'])
            thread.append(repliedTo.data['text'])
            intro = f"Generated summary; Credits: @{(repliedTo.includes['users'][0].username)}" if intro == '' else intro
            repliedTo = repliedTo.data['referenced_tweets'][-1].id if repliedTo.data['referenced_tweets'] != None and repliedTo.data['referenced_tweets'][-1].type == 'replied_to' else None    
        
        thread = '\n'.join(thread[::-1])

        return intro, thread

    def on_tweet(self, tweet):
        if 'summarize' in tweet.data['text'].split(' '):
            print('Fetching thread')
            intro, thread = self._get_thread(tweet)
            print(intro)
            summary = generate.generate_summary_t5(thread)
            toTweet = intro + '\n' + summary

            if len(toTweet) <= 280:
                self.api.update_status(status=toTweet,in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True)
            else:
                generate.write_to_image(summary=summary)
                self.api.update_status_with_media(status=intro,in_reply_to_status_id=tweet.id, filename='assets/summary_image.jpg', auto_populate_reply_metadata = True)

        
        time.sleep(0.2)
        pass


stream = Stream(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
stream.add_rules(tweepy.StreamRule(['@TheTLDRBot is:reply']))
stream.filter(tweet_fields = ['conversation_id', 'referenced_tweets'])
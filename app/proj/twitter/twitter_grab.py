__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

import tweepy
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener


################## ADD TO REQUIREMENTS
TW_CONSUMER_KEY = 'wTuKyRmRowSc5iW4D9LnwRmk4'
TW_CONSUMER_SECRET = 'hm60EEX6bns3XpAJn6ag44ts67l56MMY10mZLBNaeLBhxrt7ze'
TW_ACCESS_TOKEN = '361951128-Lnd9ZHCBcdnBifYyp8ijOTUwzZIsux3dCkc2lvjW'
TW_ACCESS_TOKEN_SECRET = 'rniZMJXxb9CVGl2NhVlaKBLE6rWOLYnTz4HjkJlz5HfgZ'

auth = OAuthHandler(TW_CONSUMER_KEY,
                    TW_CONSUMER_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN,
                      TW_ACCESS_TOKEN_SECRET)

################## ADD TO REQUIREMENTS
"""
class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True
"""
# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=['#python'])

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text
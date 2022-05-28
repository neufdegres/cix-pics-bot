import os
import twitter

def getApi():
    return twitter.Api(consumer_key = os.environ['consumer_key_cpb'],
                    consumer_secret = os.environ['consumer_secret_cpb'],
                    access_token_key = os.environ['access_token_key_cpb'],
                    access_token_secret = os.environ['access_token_secret_cpb'])

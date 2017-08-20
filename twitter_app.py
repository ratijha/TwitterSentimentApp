import tweepy
from textblob import TextBlob
import re
from textblob.sentiments import NaiveBayesAnalyzer
consumer_key = 'kxgMs6XFywD0A7E2ANt56N98H'
consumer_secret= '1TmOnK7Sts4GO6eRDm0rfF9sT6croMT2PumUyUSi6RInG2RcmB'
access_token = '3272548176-ZcEeg1jsWuYgDhzlQlSttr6pFboftycNv7N92Zw'
access_token_secret = 'j6LHL5353xvhXwOD2rv3BNAG3B1ofQdRSLRL19qhPiMda'
__author__ = 'ratijha'


class MyTwitterApp(object):

    def __init__(self):
        '''Initialize the twitter app'''
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_tweets(self, search_st):
        '''Search the tweets'''
        tweets = []
        try:
            raw_tweets = self.api.search(search_st,lang='en', count=200)
            for tweet in raw_tweets:
                # print(tweet.text)
                parsed_tweet = {}
                parsed_tweet['text'] = self.clean_tweet(tweet.text)
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet['text'] not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    if parsed_tweet['text'] not in tweets:
                        tweets.append(parsed_tweet)

        except tweepy.TweepError as e:
            raise Exception
        return tweets

    def get_tweet_sentiment(self, text):
        '''Get the sentiment of the tweet'''
        # blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        blob = TextBlob(self.clean_tweet(text))
        stmt = blob.sentiment
        if stmt.polarity > 0:
            return 'positive'
        elif stmt.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

        # return blob.sentiment.classification

# if __name__ == '__main__':
#     twit_app = MyTwitterApp()
#     tws = twit_app.get_tweets('Jab Harry Met Sejal Review')
#     # print(tws)
#     # for tw in tws:
#     #     print(tw)
#     ptweets = [t for t in tws if t['sentiment'] == 'positive']
#     print("Percentage of Positive tweets: {0} %".format(100*len(ptweets)/len(tws)))
#     ntweets = [t for t in tws if t['sentiment'] == 'negative']
#     print("Percentage of Negative  tweets: {0} %".format(100 * len(ntweets) / len(tws)))
#     print('\n')
#     print("========================================================")
#     print("Top 10 Positive tweets")
#     for t in ptweets[:10]:
#         print(t['text'])
#     print('\n')
#     print("========================================================")
#     print("Top 10 Negative tweets")
#     for t in ntweets[:10]:
#         print(t['text'])
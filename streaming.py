import tweepy
import os

auth = tweepy.OAuth1UserHandler(
os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET_KEY'], os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_SECRET_ACCESS_TOKEN']
)
streaming_client = tweepy.StreamingClient(os.environ['TWITTER_BEARER_TOKEN'])

streaming_client.sample()

api = tweepy.API(auth)
public_tweets = api.home_timeline()
for tweet in public_tweets:
	print(tweet.text)

streaming_client = tweepy.StreamingClient(os.environ['TWITTER_BEARER_TOKEN'])
streaming_client.sample()

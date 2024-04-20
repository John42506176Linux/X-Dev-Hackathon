import tweepy
import os

auth = tweepy.OAuth1UserHandler(
os.environ['X_API_KEY'], os.environ['X_API_SECRET_KEY'], os.environ['X_ACCESS_TOKEN'], os.environ['X_SECRET_ACCESS_TOKEN']
)
streaming_client = tweepy.StreamingClient(os.environ['X_BEARER_TOKEN'])

streaming_client.sample()

api = tweepy.API(auth)
public_tweets = api.home_timeline()
for tweet in public_tweets:
	print(tweet.text)

streaming_client = tweepy.StreamingClient(os.environ['X_BEARER_TOKEN'])
streaming_client.sample()

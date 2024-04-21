import os
import sys
import json
import requests

def get_twitter_user_by_username(username, bearer_token):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_user_tweets(user_id, bearer_token):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_user_likes(user_id, bearer_token):
    url = f"https://api.twitter.com/2/users/{user_id}/liked_tweets"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_tweets_and_likes(username: str):
    bearer_token = os.environ["TWITTER_BEARER_TOKEN"]
    user_id_res = get_twitter_user_by_username(username, bearer_token)
    user_id = user_id_res['data']['id']

    user_tweets = get_user_tweets(user_id, bearer_token)
    tweet_data = user_tweets['data']

    user_likes = get_user_likes(user_id, bearer_token)
    likes_data = user_likes['data']
	
    tweet_data.extend(likes_data)

    return tweet_data

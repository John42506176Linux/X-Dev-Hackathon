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

if __name__ == "__main__":
    bearer_token = os.environ["TWITTER_BEARER_TOKEN"]
    username = sys.argv[1]

    user_id_res = get_twitter_user_by_username(username, bearer_token)
    user_id = user_id_res['data']['id']

    user_tweets = get_user_tweets(user_id, bearer_token)
    tweet_data = user_tweets['data']
    print(tweet_data)

    user_likes = get_user_likes(user_id, bearer_token)
    print(user_likes)


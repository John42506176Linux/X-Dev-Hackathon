import requests
import json
import os
import sys

def get_user_id_from_tweet_id(tweet_id, bearer_token):
    """
    Given a tweet ID, returns the user ID of the tweet's author.

    :param tweet_id: The ID of the tweet
    :param bearer_token: A valid Twitter API bearer token
    :return: The user ID of the tweet's author
    """
    url = f"https://api.twitter.com/2/tweets?ids={tweet_id}&expansions=author_id&user.fields=profile_image_url,created_at"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        user = data['includes']['users'][0]
        print(user)
    else:
        print('FAILED')
        print(response.json())
        return None

if __name__ == "__main__":
	bearer_token = os.environ["TWITTER_BEARER_TOKEN"]
	tweet_id = sys.argv[1]

	get_user_id_from_tweet_id(tweet_id, bearer_token)


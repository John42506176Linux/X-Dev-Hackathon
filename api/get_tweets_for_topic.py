import os
import requests
from pinecone import Pinecone

def get_top_k_images(vector=None,k=10):
    # print(vector)
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("streamed-images")

    query_results = index.query(
        vector=[0.1] * 1408 if vector is None else vector,
        top_k=k,
        include_metadata=True
    )
    image_urls = [query_result['metadata']['image'] for query_result in query_results['matches']]
        
    return image_urls

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
        return user
        # print(user)
    else:
        print('FAILED')
        print(response.json())
        return None

def get_top_k_tweets(vector=None,k=10):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("streamed-tweets")

    query_results = index.query(
        vector=[0.1] * 1408 if vector is None else vector,
        top_k=k*2,
        include_metadata=True
    )
    tweet_info= []
    
    for query_result in query_results['matches']:
        user_info = get_user_id_from_tweet_id(query_result['id'],os.environ["TWITTER_BEARER_TOKEN"])

        if user_info is not None:
            tweet_info.append((query_result['metadata']['text'],user_info))
    
    return tweet_info[:k]

def get_full_topic_info(topics):
    return [
        {
            'representation': repres,
            'top_image': get_top_k_images(embedding, k=1),
            'top_tweets': get_top_k_tweets(embedding, k=3)
        }
        for repres, embedding in topics
    ]
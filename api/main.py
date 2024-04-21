import os
from fastapi import FastAPI
from user_tweets import get_tweets_and_likes, get_twitter_user_by_username
from text_embedding import get_text_embedding
from topic_modeling import generate_topics
from upload_to_pinecone import upload_embedding

app = FastAPI()

@app.get("/username")
async def get_username(username: str):
    bearer_token = os.environ["TWITTER_BEARER_TOKEN"]
    user_id = get_twitter_user_by_username(username, bearer_token)['data']['id']
    tweets = get_tweets_and_likes(username)

    embeddings = []
    text_list = []
    for tweet in tweets:
        tweet_embedding = get_text_embedding(tweet['text'])
        if not tweet_embedding: continue
        embeddings.append(tweet_embedding)
        text_list.append(tweet['text'])

    topic_embeddings = generate_topics(embeddings, text_list)

    pinecone_values = list()
    for i, emb in enumerate(topic_embeddings):
        pinecone_values.append({
            'id': str(i),
            'metadata': {'user_id': str(user_id)},
            'values': emb
        })

    upload_embedding(pinecone_values)

    return {"success": True}


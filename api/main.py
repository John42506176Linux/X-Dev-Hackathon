from fastapi import FastAPI
from user_tweets import get_tweets_and_likes
from text_embedding import get_text_embedding
from topic_modeling import generate_topics

app = FastAPI()

@app.get("/username")
async def get_username(username: str):
    tweets = get_tweets_and_likes(username)

    embeddings = []
    text_list = []
    for tweet in tweets:
        tweet_embedding = get_text_embedding(tweet['text'])
        if not tweet_embedding: continue
        embeddings.append(tweet_embedding)
        text_list.append(tweet['text'])

    topic_embeddings = generate_topics(embeddings, text_list)

    return {"num_topics": len(topic_embeddings)}


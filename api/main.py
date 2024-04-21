import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from user_tweets import get_tweets_and_likes, get_twitter_user_by_username
from text_embedding import get_text_embedding
from topic_modeling import generate_topics
from upload_to_pinecone import upload_embedding
from get_tweets_for_topic import get_full_topic_info, get_top_k_tweets, get_top_k_images
from get_topics_from_pinecone import query_for_user
from fastapi.middleware.cors import CORSMiddleware
import vertexai
import random
from copy import copy

app = FastAPI()

origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vertexai.init(project='x-dev-hackath', location="us-central1")

TOPIC_RANKING = {}
SEEN = set()

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

    topic_embeddings, topics = generate_topics(embeddings, text_list)

    pinecone_values = list()
    for i, emb in enumerate(topic_embeddings):
        pinecone_values.append({
            'id': str(i),
            'metadata': {'user_id': str(user_id), 'topic': topics[i]},
            'values': emb
        })

    upload_embedding(pinecone_values, 'test-index')
    return {"user_id": user_id}

@app.get("/initial_topics/{user_id}")
async def get_initial_topics(user_id: str):
    # if user_id in SEEN:
    #     return {"data": []}
    SEEN.add(user_id)
    topics = query_for_user(user_id)
    a = get_full_topic_info(topics)
    global TOPIC_RANKING
    TOPIC_RANKING[user_id] = [i[0] for i in topics]
    return {"data": a}

@app.get("/topic_ranking/{user_id}")
async def get_topic_ranking(user_id: str):
    global TOPIC_RANKING
    new_ranking = copy(TOPIC_RANKING[user_id])
    item = random.choice(TOPIC_RANKING[user_id])
    try:
        index = TOPIC_RANKING[user_id].index(item)
        
        if index > 0:
            new_position = random.randint(0, index - 1)
            new_ranking.pop(index)
            new_ranking.insert(new_position, item)
            print(f"Moved '{item}' from position {index} to {new_position}")
        else:
            print(f"Item '{item}' is already at the top of the list")
    except ValueError:
        return {"order": TOPIC_RANKING[user_id]}
    else:
        TOPIC_RANKING[user_id] = new_ranking
        return {"order": new_ranking}

@app.get("/get_new_data/{user_id}")
async def get_new_data(user_id: str):
    topic_embeddings = query_for_user(user_id)
    topics = [i[0] for i in topic_embeddings]
    
    a = get_full_topic_info(topics)
    return {"data": a}

    
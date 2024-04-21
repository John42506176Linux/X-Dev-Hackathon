import os
# import requests
# import asyncio
# import pandas as pd
# import numpy as np
# import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from user_tweets import get_tweets_and_likes, get_twitter_user_by_username
from text_embedding import get_text_embedding
from topic_modeling import generate_topics
from upload_to_pinecone import upload_embedding
from get_tweets_for_topic import get_full_topic_info
# from get_stream_tweets_images import (
#     bearer_oauth,
#     get_tweet_image_from_id,
#     remove_twitter_images,
#     River,
# 	PROMPT,
# 	is_english,
# 	set_rules,
# )
from get_topics_from_pinecone import query_for_user
# from test_embeddings import get_image_embeddings
# from river import stream
# from river import cluster
# from bertopic.vectorizers import OnlineCountVectorizer
# from bertopic.vectorizers import ClassTfidfTransformer
# import openai
# import tiktoken
# from bertopic import BERTopic
# from bertopic.representation import OpenAI
# from pinecone import Pinecone

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
    topics = query_for_user(user_id)
    a = get_full_topic_info(topics)
    print(a)
	# return {"topics": topics}

# @app.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: str):
# 	await websocket.accept()
# 	try:
# 		topics = query_for_user(user_id)
# 		set_rules(topics)

# 		headers = {"x-b3-flags": '1'}
# 		response = requests.get(
# 			"https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, headers=headers, stream=True,
# 		)
# 		print(response.status_code)
# 		if response.status_code != 200:
# 			print(response.headers)
# 			raise Exception(
# 				"Cannot get stream (HTTP {}): {}".format(
# 					response.status_code, response.text
# 				)
# 			)
# 		tweets_data = []
# 		cluster_model = River(cluster.DBSTREAM())
# 		vectorizer_model = OnlineCountVectorizer(stop_words="english")
# 		ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True, bm25_weighting=True)
# 		tokenizer= tiktoken.encoding_for_model("gpt-3.5-turbo")
# 		client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
# 		representation_model = OpenAI(
# 			client,
# 			model="gpt-3.5-turbo", 
# 			delay_in_seconds=2, 
# 			chat=True,
# 			nr_docs=4,
# 			doc_length=100,
# 			tokenizer=tokenizer,
# 			prompt=PROMPT
# 		)
# 		pd.set_option('display.max_rows', None)       # No limit on the number of rows displayed
# 		pd.set_option('display.max_columns', None)    # No limit on the number of columns displayed
# 		pd.set_option('display.width', None)          # Automatically set the display width to accommodate the maximum line width
# 		pd.set_option('display.max_colwidth', None)   # Display the full content of each column without truncation
# 		for response_line in response.iter_lines():
# 			if response_line:
# 				json_response = json.loads(response_line)

# 				tweet_id = json_response["data"]["id"]

# 				# Get the image URL from the tweet ID (implement this function)
# 				image_url = get_tweet_image_from_id(tweet_id)

# 				# Remove image links from the tweet text (implement this function)
# 				cleaned_text = remove_twitter_images(json_response["data"]["text"])

# 				tweets_data.append((image_url, cleaned_text, tweet_id))

# 				topic_model = BERTopic(
# 					hdbscan_model=cluster_model, 
# 					vectorizer_model=vectorizer_model, 
# 					ctfidf_model=ctfidf_model,
# 					representation_model=representation_model,
# 					min_topic_size=10
# 				)
# 				print(f"Number of Tweets:{len(tweets_data)}")
# 				print(f'Tweet:{json_response["data"]["text"]}')
# 				print(f'Tweet Language:{is_english(json_response["data"]["text"])}')
# 				if len(tweets_data) == 15:
# 					try:
# 						cleaned_tweets_data = [(image,tweet,tweetid) for image,tweet,tweetid in tweets_data if tweet != '' and is_english(tweet) ]
# 						cleaned_images_data = [(image,tweet,tweetid) for image,tweet,tweetid in tweets_data if image is not None]
# 						tweets = [tweet for image, tweet, tweetid in cleaned_tweets_data]
# 						tweet_ids = [tweetid for image, tweet, tweetid in cleaned_tweets_data]
# 						tweet_embeddings = [get_image_embeddings(image,tweet) for image,tweet,tweetid in cleaned_tweets_data ]
# 						text_embeddings =[embedding[1] for embedding in tweet_embeddings]

# 						images = [image for image, tweet, tweetid in cleaned_images_data]
# 						image_embeddings = [get_image_embeddings(image,tweet) for image,tweet,tweetid in cleaned_images_data ]
# 						image_embeddings = [embedding[0] for embedding in image_embeddings]
# 						# print("Embedded tweets")
# 						print(f"Cleaned tweets:{len(tweets)}")
# 						topic_model.partial_fit(tweets,embeddings=np.array(text_embeddings))
# 						topic_names = [name[2:] for name in topic_model.get_topic_info()['Name']]
# 						await websocket.send_json({"topics": topic_names})
# 						print(topic_model.get_topic_info())
# 					except Exception as e:
# 						print(f'Error: {e}')
# 						print("Couldn't update model")

# 					try:
# 						# Upload to pinecone
# 						values = [{
# 							'id': tweetid,
# 							'metadata': {'text': tweet},
# 							'values': tweet_emb
# 						} for tweetid, tweet, tweet_emb in zip(tweet_ids, tweets, text_embeddings)]
# 						upload_embedding(values, 'streamed-tweets-2')
# 						print(f'Uploaded {len(values)} tweets to pinecone')

# 						# Upload image embeddings with image_link as metadata (saes in cleaned_images_data)
# 						values = [{
# 							'id': tweetid,
# 							'metadata': {'image': image},
# 							'values': image_emb
# 						} for tweetid, image, image_emb in zip(tweet_ids, images, image_embeddings)]
# 						if values:
# 							upload_embedding(values, 'streamed-images')
# 						print(f'Uploaded {len(values)} images to pinecone')
# 					except Exception as e:
# 						print("Couldn't upload to pinecone")

# 					tweets_data.clear()
# 	except WebSocketDisconnect:
# 		print(f"WebSocket with user_id {user_id} disconnected")


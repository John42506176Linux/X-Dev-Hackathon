import requests
import os
import json
import time
import random
from dotenv import load_dotenv
import re
from PIL import Image
import requests
from io import BytesIO
from river import stream
from river import cluster
from bertopic.vectorizers import OnlineCountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic import BERTopic
from test_embeddings import get_image_embeddings
import numpy as np
from bertopic.representation import OpenAI
import openai
import tiktoken
import pandas as pd
from langdetect import detect, LangDetectException


load_dotenv()  

def is_english(text):
    try:
        # Detect the language of the text
        return detect(text) == 'en'
    except LangDetectException:
        # Handle exception if text is too short or any other issue with langdetect
        return False

PROMPT = """
I have topic that contains the following documents: \n[DOCUMENTS]
The topic is described by the following keywords: [KEYWORDS]

Based on the above information, can you give a short label of the topic?

The topics should have optinions based on the documents and keywords. Here are some examples of topics:
    - Who Will the Bengals Draft?
    - Earth on a Record Hot Streak
    - Senate Authorizes Controversial Surveillance Program
    - Jujutsu Kaisen -  Nah, I'd Pass
    - Netflix's One Piece Review: A Not-Quite Grand Line
    - Humane AI Pin Reveals its Fatal Flaw

Keep the topic down to about 5 words and make sure it is immediately usable as a title.
"""

class River:
    def __init__(self, model):
        self.model = model

    def partial_fit(self, umap_embeddings):
        for umap_embedding, _ in stream.iter_array(umap_embeddings):
            self.model.learn_one(umap_embedding)

        labels = []
        for umap_embedding, _ in stream.iter_array(umap_embeddings):
            label = self.model.predict_one(umap_embedding)
            labels.append(label)

        self.labels_ = labels
        return self

# To set your enviornment variables in your terminal run the following line:
bearer_token = os.environ['TWITTER_BEARER_TOKEN']


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(f"Twitter Rules:{json.dumps(response.json())}")
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(topic):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": f"{topic}"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))

def remove_twitter_images(text):
    # This pattern matches URLs like "https://t.co/..." which are typically used for Twitter images or links
    pattern = r"https://t.co/[A-Za-z0-9]+"
    # Replace the matched URLs with an empty string
    cleaned_text = re.sub(pattern, '', text)
    # Remove any extra spaces and newlines that may be left behind
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def get_tweet_image_from_id(id):
    tweet_fields = "expansions=attachments.media_keys&media.fields=duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width,alt_text"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = f"ids={id}"
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    try:
        response = requests.request("GET", url, auth=bearer_oauth)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()['includes']['media'][0]['url']
    except Exception as e:
        return None

def get_filtered_stream():
    headers = {"x-b3-flags": '1'}
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        print(response.headers)
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    tweets_data = []
    cluster_model = River(cluster.DBSTREAM())
    vectorizer_model = OnlineCountVectorizer(stop_words="english")
    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True, bm25_weighting=True)
    tokenizer= tiktoken.encoding_for_model("gpt-3.5-turbo")
    client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    representation_model = OpenAI(
        client,
        model="gpt-3.5-turbo", 
        delay_in_seconds=2, 
        chat=True,
        nr_docs=4,
        doc_length=100,
        tokenizer=tokenizer,
        prompt=PROMPT
    )
    pd.set_option('display.max_rows', None)       # No limit on the number of rows displayed
    pd.set_option('display.max_columns', None)    # No limit on the number of columns displayed
    pd.set_option('display.width', None)          # Automatically set the display width to accommodate the maximum line width
    pd.set_option('display.max_colwidth', None)   # Display the full content of each column without truncation
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)

            tweet_id = json_response["data"]["id"]

            # Get the image URL from the tweet ID (implement this function)
            image_url = get_tweet_image_from_id(tweet_id)

            # Remove image links from the tweet text (implement this function)
            cleaned_text = remove_twitter_images(json_response["data"]["text"])

            tweets_data.append((image_url, cleaned_text))

            topic_model = BERTopic(
                hdbscan_model=cluster_model, 
                vectorizer_model=vectorizer_model, 
                ctfidf_model=ctfidf_model,
                representation_model=representation_model,
                min_topic_size=10
            )
            print(f"Number of Tweets:{len(tweets_data)}")
            print(f'Tweet:{json_response["data"]["text"]}')
            print(f'Tweet Language:{is_english(json_response["data"]["text"])}')
            if len(tweets_data) == 15:
                try:
                    cleaned_tweets_data = [(image,tweet) for image,tweet in tweets_data if tweet != '' and is_english(tweet) ]
                    cleaned_images_data = [(image,tweet) for image,tweet in tweets_data if image is not None]
                    tweets = [tweet for image, tweet in cleaned_tweets_data]
                    tweet_embeddings = [get_image_embeddings(image,tweet) for image,tweet in cleaned_tweets_data ]
                    text_embeddings =[embedding[1] for embedding in tweet_embeddings]
                    # image_embeddings = [embedding[0] for embedding in tweet_embeddings]
                    # print("Embedded tweets")
                    print(f"Cleaned tweets:{len(tweets)}")
                    topic_model.partial_fit(tweets,embeddings=np.array(text_embeddings))
                    topic_model.topic_embeddings_
                    print(topic_model.get_topic_info())
                    
                except Exception as e:
                    print("Couldn't update model")
                tweets_data.clear()

                

def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set_rules('LAKERS')
    get_filtered_stream()

if __name__ == "__main__":
    main()

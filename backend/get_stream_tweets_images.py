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

load_dotenv()  


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
        {"value": f"{topic} has:images"},
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

    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()['includes']['media'][0]['url']

def get_stream():
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
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            id = json_response["data"]["id"]

            print(f"Image:{get_tweet_image_from_id(id)}")
            # print(json.dumps(json_response, indent=4, sort_keys=True))
            print(f'Text:{remove_twitter_images(json_response["data"]["text"])}')

def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set_rules('#420day')
    get_stream()

if __name__ == "__main__":
    main()

import os
import math
import numpy as np
from hdbscan import HDBSCAN
from bertopic import BERTopic
import openai
import tiktoken
from bertopic.representation import OpenAI

PROMPT = """
I have topic that contains the following documents: \n[DOCUMENTS]
The topic is described by the following keywords: [KEYWORDS]

Based on the above information, can you give a short label of the topic?

The topic should be 1 or 2 words max, here are some examples:
    - Bengals
    - Climate Change
    - FISA
    - JJK
    - One Piece
    - Humane AI
"""

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

Keep the topic down to about 5-6 words and make sure it is immediately usable as a title.
"""

def generate_topics(embeddings: list, text: list):
	embeddings = np.array(embeddings)
	text = np.array(text)

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

	hdbscan_model = HDBSCAN(
		min_cluster_size=2,
		metric='euclidean',
		cluster_selection_method='eom',
		prediction_data=True
	)

	topic_model = BERTopic(
		representation_model=representation_model,
		verbose=True,
		hdbscan_model=hdbscan_model,
		min_topic_size=4
	)

	topics, probs = topic_model.fit_transform(
		embeddings=embeddings,
		documents=text
	)

	topic_names = list(topic_model.get_topic_info()['Name'])
	topics = list()
	# each topic starts with a number_ like '0_topic' so remove it with a log 10 function
	for i, topic in enumerate(topic_names):
		index_len = math.floor(math.log10(i)) + 1 if i else 1
		topics.append(topic[index_len+1:])

	return topic_model.topic_embeddings_, topics


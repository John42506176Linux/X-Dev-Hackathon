import os
from pinecone import Pinecone
from dotenv import load_dotenv
from get_user_info_from_tweet import get_user_id_from_tweet_id
load_dotenv()  

def get_top_k_tweets(vector=None,k=10):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("streamed-tweets")

    query_results = index.query(
        vector=[0.1] * 1408 if vector is None else vector.tolist(),
        top_k=k*2,
        include_metadata=True
    )
    tweet_info= []
    
    for query_result in query_results['matches']:
        try:
            user_info = get_user_id_from_tweet_id(query_result['id'],os.environ["TWITTER_BEARER_TOKEN"])

            if user_info is not None:
                tweet_info.append((query_result['metadata']['text'],user_info))
        except Exception as e:
            print(f'Missed:{e}')
    
    return tweet_info[:k]

def get_top_similarity_score(vector,user_id):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("test-index")

    x = index.query(
        vector=vector.tolist(),
        filter={
            "user_id": {"$eq": user_id},
        },
        top_k=10,
        include_metadata=True
    )['matches'][0]['score']

    return x

def get_top_k_images(vector=None,k=10):
    print(vector)
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("streamed-images")

    query_results = index.query(
        vector=[0.1] * 1408 if vector is None else vector.tolist(),
        top_k=k,
        include_metadata=True
    )
    image_urls = [query_result['metadata']['image'] for query_result in query_results['matches']]
        
    return image_urls

if __name__ == "__main__":
    print(len(get_top_k_tweets()))

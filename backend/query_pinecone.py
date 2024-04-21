import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()  

def get_top_similarity_score(vector=None):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("test-index")

    x = index.query(
        vector=[0.1] * 1408 if not vector else vector,
        filter={
            "user_id": {"$eq": "3293358400"},
        },
        top_k=5,
        include_metadata=True
    )['matches'][0]['score']

    return x

def get_top_k_images(vector=None,k=10):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("image-index")

    query_results = index.query(
        vector=[0.1] * 1408 if not vector else vector,
        top_k=k,
        include_metadata=True
    )
    image_urls = [query_result['metadata']['image'] for query_result in query_results]
        
    return image_urls

def get_top_similarity_score(vector):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("test-index")

    x = index.query(
        vector=vector,
        filter={
            "user_id": {"$eq": "3293358400"},
        },
        top_k=5,
        include_metadata=True
    )['matches'][0]['score']

    return x

def get_top_k_images(vector,k=10):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("streamed-images")

    query_results = index.query(
        vector=[0.1] * 1408 if not vector else vector,
        top_k=k,
        include_metadata=True
    )
    image_urls = [query_result['metadata']['image'] for query_result in query_results]
        
    return image_urls

if __name__ == "__main__":
    print(get_top_similarity_score())

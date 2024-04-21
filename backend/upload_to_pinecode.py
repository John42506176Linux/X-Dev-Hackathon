import os
import numpy as np
from pinecone import Pinecone

def upload_embedding(vectors, index_name, pinecone):
    index = pinecone.Index(index_name)
    index.upsert(vectors=vectors)

if __name__ == "__main__":
    api_key = os.environ["PINECONE_API_KEY"]
    pinecone = Pinecone(api_key=api_key)

    embedding = np.load('embedding.npy')
    vectors = [{"id": "test", "values": embedding}]
    upload_embedding(vectors, "test-index", pinecone)

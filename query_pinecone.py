import os
from pinecone import Pinecone

def get_top_similarity_score(vector=None):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("test-index")

    x = index.query(
        vector=[0.1] * 1408 if not vector else vector,
        filter={
            "user_id": {"$eq": "3293358400"},
        },
        top_k=1,
        include_metadata=True
    )

    return x

print(get_top_similarity_score())

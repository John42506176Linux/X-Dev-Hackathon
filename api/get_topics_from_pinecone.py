import os
import sys
from pinecone import Pinecone

def query_for_user(user_id):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index("test-index")

    x = index.query(
        vector=[0.1] * 1408,
        filter={
            "user_id": {"$eq": user_id},
        },
        top_k=100,
        include_metadata=True,
        include_values=True
    )

    topics = [i['metadata']['topic'].strip('"') for i in x['matches']]
    values = [i['values'] for i in x['matches']]

    return list(zip(topics, values))

if __name__ == "__main__":
    user_id = sys.argv[1]
    print(query_for_user(user_id))
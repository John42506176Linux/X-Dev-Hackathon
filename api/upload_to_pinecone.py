def upload_embedding(vectors):
    api_key = os.environ["PINECONE_API_KEY"]
    pinecone = Pinecone(api_key=api_key)

    index = pinecone.Index('text-index')
    index.upsert(vectors=vectors)

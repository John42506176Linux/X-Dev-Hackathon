from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from typing import List, Optional
from google.auth import credentials as auth_credentials
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  

def embed_text(
    texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
    task: str = "RETRIEVAL_DOCUMENT",
    model_name: str = "textembedding-gecko@003",
) -> List[List[float]]:
    """Embeds texts with a pre-trained, foundational model."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    embeddings = model.get_embeddings(inputs)
    return [embedding.values for embedding in embeddings]
# print(embed_text())

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

message = "What are some of the pros and cons of Python as a programming language?"
print(model.invoke(message).content)
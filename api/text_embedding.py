import re
import os
from vertexai.vision_models import MultiModalEmbeddingModel, MultiModalEmbeddingResponse

def remove_twitter_images(text: str):
    # This pattern matches URLs like "https://t.co/..." which are typically used for Twitter images or links
    pattern = r"https://t.co/[A-Za-z0-9]+"
    # Replace the matched URLs with an empty string
    cleaned_text = re.sub(pattern, '', text)
    # Remove any extra spaces and newlines that may be left behind
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def get_text_embedding(text: str) -> MultiModalEmbeddingResponse:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    text = remove_twitter_images(text)
    if not text: return

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    embeddings = model.get_embeddings(contextual_text=text)

    return embeddings.text_embedding


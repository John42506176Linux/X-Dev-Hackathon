from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from typing import List, Optional
from google.auth import credentials as auth_credentials
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from PIL import Image 
import requests
from io import BytesIO
from vertexai.vision_models import (
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
    Video,
    VideoSegmentConfig,
    Image as GoogleImage
)

import vertexai
import os


load_dotenv()  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

def get_image_data(
    url: str,
):
    # Fetch the image
    response = requests.get(url)
    content_type = response.headers['content-type']
    format = {'image/png': 'PNG', 'image/jpeg': 'JPEG', 'image/webp': 'WEBP'}.get(content_type, 'JPEG')  # Default to JPEG if unknown

    img = Image.open(BytesIO(response.content))

    # Resize the image
    img_resized = img.resize((256, 256))

    # Save the resized image to a bytes buffer
    img_byte_arr = BytesIO()
    img_resized.save(img_byte_arr, format=format)  # Use the dynamic format

    # Get the byte data
    return img_byte_arr.getvalue()

def get_video_data(url: str):
    # Fetch the video
    response = requests.get(url)
    
    # Ensure the request was successful
    if response.status_code != 200:
        raise ValueError(f"Failed to download video: HTTP {response.status_code}")
    
    # Ensure the content type is a video
    content_type = response.headers['content-type']
    if 'video' not in content_type:
        raise ValueError("URL must be a video, found content type: {}".format(content_type))

    # Get the byte data
    return response.content


vertexai.init(project='x-dev-hackath', location="us-central1")

def get_video_embeddings(
    video_path: str = None,
    contextual_text: Optional[str] = None
):

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    video = None
    if video_path:
        video = get_video_data(video_path)

    if video is not None:
        embeddings = model.get_embeddings(
            video=Video(video),
            video_segment_config=None,
            contextual_text=contextual_text,
            dimension=1408,
        )
    else:  
        embeddings = model.get_embeddings(
            contextual_text=contextual_text,
            dimension=1408,
        )
    # Video Embeddings are segmented based on the video_segment_config.
    return (embeddings.video_embeddings[0].embedding,embeddings.text_embedding)
    
def get_image_embeddings(
    image_path: str = None,
    contextual_text: Optional[str] = None,
) -> MultiModalEmbeddingResponse:
    """Example of how to generate multimodal embeddings from image and text.

    Args:
        project_id: Google Cloud Project ID, used to initialize vertexai
        location: Google Cloud Region, used to initialize vertexai
        image_path: Path to image (local or Google Cloud Storage) to generate embeddings for.
        contextual_text: Text to generate embeddings for.
    """

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    if image_path:
        image = get_image_data(image_path)

    if image_path is not None:
        embeddings = model.get_embeddings(
            image=GoogleImage(image),
            contextual_text=contextual_text,
        )
    else:
        embeddings = model.get_embeddings(
            contextual_text=contextual_text,
        )
    return (embeddings.image_embedding,embeddings.text_embedding)

# def embed_text(
#     texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
#     task: str = "RETRIEVAL_DOCUMENT",
#     model_name: str = "textembedding-gecko@003",
# ) -> List[List[float]]:
#     """Embeds texts with a pre-trained, foundational model."""
#     model = TextEmbeddingModel.from_pretrained(model_name)
#     inputs = [TextEmbeddingInput(text, task) for text in texts]
#     embeddings = model.get_embeddings(inputs)
#     return [embedding.values for embedding in embeddings]

if __name__ == "__main__":
    # print(embed_text())
    embeddings= get_video_embeddings('https://video.twimg.com/tweet_video/GLsnJUqakAA5pG_.mp4','@im_right_though 😂😂😂')
    print(f"Video Embeddings:{len(embeddings[0])}")
    print(f"Text Embeddings:{len(embeddings[1])}")


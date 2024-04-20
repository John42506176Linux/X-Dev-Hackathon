import vertexai
from vertexai.generative_models import GenerativeModel, Part,Image
import os
from dotenv import load_dotenv
import http.client
import typing
import urllib.request

load_dotenv()  

vertexai.init(project=os.environ['PROJECT_ID'], location="us-central1")

model = GenerativeModel("gemini-pro-vision")

# video_file_uri = "gs://cloud-samples-data/generative-ai/video/behind_the_scenes_pixel.mp4"
# video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")

def load_image_from_url(image_url: str) -> Image:
    with urllib.request.urlopen(image_url) as response:
        response = typing.cast(http.client.HTTPResponse, response)
        image_bytes = response.read()
    return Image.from_bytes(image_bytes)

# Load images from Cloud Storage URI
landmark1 = load_image_from_url(
    "https://storage.googleapis.com/cloud-samples-data/vertex-ai/llm/prompts/landmark1.png"
)
image_file_uri = "GLin2EqXIAAjLR4.png"
with open(image_file_uri, "rb") as img_file:
    image_file = img_file.read()

prompt = """
  What is in the image
"""

contents = [
    # video_file,
    landmark1,
    prompt,
]

response = model.generate_content(contents)
print(response.text)
import base64
import azure.identity
from azure.identity import DefaultAzureCredential, get_bearer_token_provider  
from PIL import Image
import openai
import os
from dotenv import load_dotenv
import json
openai_credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(openai_credential, "https://cognitiveservices.azure.com/.default")

load_dotenv()
azure_openai_key=os.getenv("AZURE_OPENAI_KEY")
azure_openai_endpoint="https://nikhi-m3y8inyh-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

def read_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def resize_image(image_path, max_width=800, max_height=800):
    with Image.open(image_path) as img:
        img.thumbnail((max_width, max_height))
        img.save(image_path)
    
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def generate_text(prompt_instruction,image_base64):
    client = openai.AzureOpenAI(api_key=azure_openai_key,api_version="2024-02-01",azure_endpoint=azure_openai_endpoint)


    response = client.chat.completions.create(
    model='gpt-4o',
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "provide JSON file that represents this document. Use this JSON Schema: " +
                    prompt_instruction },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ],
    max_tokens=500,
    )
    return response.choices[0].message.content




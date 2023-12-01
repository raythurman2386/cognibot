import os

from dotenv import load_dotenv
from db.database import add_message, get_chat_log
from openai import OpenAI
import cloudinary
import cloudinary.uploader
import requests
import logging

# Configure logging
from utils.utils import CustomError, handle_error

load_dotenv()

env_vars = {
    "gpt_model": os.environ.get("GPT_MODEL") or "gpt-3.5-turbo",
    "image_model": os.environ.get("IMAGE_MODEL") or "dall-e-3",
    "image_size": os.environ.get("IMAGE_SIZE") or "1024x1024",
    "image_quality": os.environ.get("IMAGE_QUALITY") or "standard",
    "cloud_name": os.environ.get('NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME'),
    "cloudinary_api_key": os.environ.get('CLOUDINARY_API_KEY'),
    "cloudinary_api_secret": os.environ.get('CLOUDINARY_API_SECRET'),
    "cloudinary_folder": os.environ.get('CLOUDINARY_FOLDER'),
    "deploy_hook": os.environ.get("DEPLOY_HOOK")
}

client = OpenAI()

cloudinary.config(
    cloud_name=env_vars["cloud_name"],
    api_key=env_vars["cloudinary_api_key"],
    api_secret=env_vars["cloudinary_api_secret"],
)


def img_generation(prompt):
    try:
        response = client.images.generate(
            model=env_vars["image_model"],
            prompt=prompt,
            size=env_vars["image_size"],
            quality=env_vars["image_quality"],
            n=1,
        )

        img_url = response.data[0].url
        return img_url
    except Exception as e:
        return handle_error(e)


def ask_gpt(question):
    try:
        if len(question) == 0:
            raise CustomError("Please provide a question for ChatGPT!")

        # Insert the user's message into the database
        add_message("user", question)

        # Retrieve the chat log from the database
        chat_log = get_chat_log()

        response = client.chat.completions.create(
            model=env_vars["gpt_model"], messages=chat_log, temperature=0.1
        )
        answer = response.choices[0].message.content

        # Insert the bot's response into the database
        add_message("assistant", answer)

        return answer
    except Exception as e:
        return handle_error(e)


def upload_image(image_url):
    folder_name = env_vars["cloudinary_folder"]
    try:
        response = cloudinary.uploader.upload(image_url, folder=folder_name)
        logging.info("Image uploaded successfully")
        deploy_gallery()
        return response
    except Exception as e:
        logging.error(f"Failed to upload image: {e}")
        raise
    

def deploy_gallery():
    deploy_hook_url = env_vars["deploy_hook"]
    
    try:
        response = requests.post(deploy_hook_url)
        if response.status_code == 201:  
            logging.info("Deploy triggered successfully")
        else:
            logging.warning(f"Failed to trigger deploy. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to trigger deploy: {e}")
        raise
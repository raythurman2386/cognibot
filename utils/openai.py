from db.database import add_message, get_chat_log
from openai import OpenAI
import cloudinary
import cloudinary.uploader
import requests
from utils.logger import app_logger
from utils.env import env_vars

# Configure logging
from utils.utils import CustomError, handle_error


client = OpenAI()

cloudinary.config(
    cloud_name=env_vars["cloud_name"],
    api_key=env_vars["cloudinary_api_key"],
    api_secret=env_vars["cloudinary_api_secret"],
)


def img_generation(prompt, quality, size):
    try:
        response = client.images.generate(
            model=env_vars["image_model"],
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        img_url = response.data[0].url
        app_logger.info("Image Successfully Generated")
        return img_url
    except Exception as e:
        app_logger.error(f"Image Generation Failed: {e}")
        return handle_error(e)


def ask_gpt(question):
    try:
        if len(question) == 0:
            raise CustomError("Please provide a question for ChatGPT!")

        # Insert the user's message into the database
        add_message("user", question)
        app_logger.info("User message added to database")

        # Retrieve the chat log from the database
        chat_log = get_chat_log()

        response = client.chat.completions.create(
            model=env_vars["gpt_model"], messages=chat_log, temperature=0.1
        )
        answer = response.choices[0].message.content
        app_logger.info("GPT Response successful")

        # Insert the bot's response into the database
        add_message("assistant", answer)
        app_logger.info("Assistant message added to database")

        return answer
    except Exception as e:
        app_logger.error("GPT generation encountered an error: {e}")
        return handle_error(e)


async def upload_image(image_url):
    folder_name = env_vars["cloudinary_folder"]
    try:
        response = await cloudinary.uploader.upload(image_url, folder=folder_name)
        app_logger.info("Image uploaded successfully")
        deploy_gallery()
        return response
    except Exception as e:
        app_logger.error(f"Failed to upload image: {e}")
        raise


def deploy_gallery():
    deploy_hook_url = env_vars["deploy_hook"]

    try:
        response = requests.post(deploy_hook_url)
        if response.status_code == 201:
            app_logger.info("Deploy triggered successfully")
        else:
            app_logger.warning(
                f"Failed to trigger deploy. Status code: {response.status_code}"
            )
    except Exception as e:
        app_logger.error(f"Failed to trigger deploy: {e}")
        raise

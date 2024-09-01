from openai import OpenAI
import cloudinary
import cloudinary.uploader
import requests
from utils.logger import app_logger
from utils.env import env_vars
from utils.utils import CustomError, handle_error


client = OpenAI()

cloudinary.config(
    cloud_name=env_vars["cloud_name"],
    api_key=env_vars["cloudinary_api_key"],
    api_secret=env_vars["cloudinary_api_secret"],
)


def img_generation(prompt, quality, size, style):
    try:
        response = client.images.generate(
            model=env_vars["image_model"],
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1,
        )

        img_url = response.data[0].url
        app_logger.info("Image Successfully Generated")
        # Download image from DALL-E URL
        img_data = requests.get(img_url).content
        app_logger.info("Image Successfully Downloaded")

        upload_result = upload_image(image_bytes=img_data)
        return upload_result["secure_url"]
    except Exception as e:
        app_logger.error(f"❌ Image Generation Failed: {e}")
        return handle_error(e)


def ask_gpt(user_id, question, db):
    try:
        if len(question) == 0:
            raise CustomError("Please provide a question for ChatGPT!")

        db.add_message(user_id, "user", question)
        app_logger.info(f"User message added to database for user {user_id}")

        chat_log = db.get_chat_log(user_id)

        response = client.chat.completions.create(
            model=env_vars["gpt_model"],
            messages=chat_log,
            temperature=0.1,
            max_tokens=2048,
        )
        answer = response.choices[0].message.content
        app_logger.info(f"ChatGPT generation successful for user {user_id}")

        db.add_message(user_id, "assistant", answer)
        app_logger.info(f"ChatGPT message added to database for user {user_id}")

        return answer
    except Exception as e:
        app_logger.error(
            f"❌ GPT generation encountered an error for user {user_id}: {e}"
        )
        return handle_error(e)


def ask_vision():
    pass


def upload_image(image_bytes):
    folder_name = env_vars["cloudinary_folder"]
    try:
        response = cloudinary.uploader.upload(image_bytes, folder=folder_name)
        app_logger.info("Image uploaded successfully")
        deploy_gallery()
        return response
    except Exception as e:
        app_logger.error(f"❌ Failed to upload image: {e}")
        return handle_error(e)


def deploy_gallery():
    deploy_hook_url = env_vars["deploy_hook"]

    try:
        response = requests.post(deploy_hook_url)
        if response.status_code == 201:
            app_logger.info("Deploy triggered successfully")
        else:
            app_logger.warning(
                f"❌ Failed to trigger deploy. Status code: {response.status_code}"
            )
    except Exception as e:
        app_logger.error(f"❌ Failed to trigger deploy: {e}")
        return handle_error(e)

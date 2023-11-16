import os

from dotenv import load_dotenv
from db.database import add_message, get_chat_log
from openai import OpenAI

load_dotenv()

env_vars = {
    "gpt_model": os.environ.get("GPT_MODEL") or "gpt-3.5-turbo",
    "image_model": os.environ.get("IMAGE_MODEL") or "dall-e-3",
    "image_size": os.environ.get("IMAGE_SIZE") or "1024x1024",
    "image_quality": os.environ.get("IMAGE_QUALITY") or "standard",
}

client = OpenAI()


class CustomError(Exception):
    pass


def handle_error(e):
    if isinstance(e, CustomError):
        return str(e)
    else:
        # Log the error or handle it as needed
        return "Blimey! Something went wrong: " + str(e)


def imgGeneration(prompt):
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


def askgpt(question):
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

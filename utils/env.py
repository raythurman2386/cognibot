"""
    Cognibot is a Discord bot built with Python and Pycord leveraging OpenAI and Anthropic
    for large language model capabilities. Currently hosted on a personal Raspberry
    Pi 4 and utilizing an SQLite database for per-user chat log storage.

    Required Environment Variables:
    - DISCORD_TOKEN
    - OPENAI_API_KEY
    - ANTHROPIC_API_KEY

    The following environment variables are optional and were previously used
    when hosting the bot on Heroku with a Postgres database:
    - DB_NAME
    - DB_USER
    - DB_PASS
    - DATABASE_URL

    The Cloudinary environment variables and deploy hook are for image generation
    and hosting. They should not cause errors with local testing but if issues arise
    they can be requested or set up personally through Cloudinary.
"""

import os
from dotenv import load_dotenv

load_dotenv()

env_vars = {
    # REQUIRED
    "token": os.environ.get(
        "DISCORD_TOKEN"
    ),  # Missing this token will result in a discord error
    "anthropic_key": os.environ.get("ANTHROPIC_API_KEY"),
    "openai_key": os.environ.get("OPENAI_API_KEY"),
    # OPTIONAL
    "gpt_model": os.environ.get("GPT_MODEL") or "gpt-3.5-turbo",
    "image_model": os.environ.get("IMAGE_MODEL") or "dall-e-3",
    "claude_model": os.environ.get("CLAUDE_MODEL") or "claude-3-haiku-20240307",
    # CLOUDINARY AND GALLERY DEPLOYMENT
    "cloud_name": os.environ.get("NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME"),
    "cloudinary_api_key": os.environ.get("CLOUDINARY_API_KEY"),
    "cloudinary_api_secret": os.environ.get("CLOUDINARY_API_SECRET"),
    "cloudinary_folder": os.environ.get("CLOUDINARY_FOLDER"),
    "deploy_hook": os.environ.get("DEPLOY_HOOK"),
    # DATABASE
    # DEPRECATED These are from a prior postgres database I was using when deployed with heroku
    # May still be useful in the future but not currently in use
    # "db_name": os.environ.get("DB_NAME"),
    # "db_user": os.environ.get("DB_USER"),
    # "db_pass": os.environ.get("DB_PASS"),
    # "db_host": os.environ.get("DB_HOST"),
    # "db_url": os.environ.get("DATABASE_URL"),
    "db_type": "sqlite",
}

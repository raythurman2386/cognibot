import os
from dotenv import load_dotenv

load_dotenv()

env_vars = {
    "gpt_model": os.environ.get("GPT_MODEL") or "gpt-3.5-turbo",
    "image_model": os.environ.get("IMAGE_MODEL") or "dall-e-3",
    "image_size": os.environ.get("IMAGE_SIZE") or "1024x1024",
    "image_quality": os.environ.get("IMAGE_QUALITY") or "standard",
    "cloud_name": os.environ.get("NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME"),
    "cloudinary_api_key": os.environ.get("CLOUDINARY_API_KEY"),
    "cloudinary_api_secret": os.environ.get("CLOUDINARY_API_SECRET"),
    "cloudinary_folder": os.environ.get("CLOUDINARY_FOLDER"),
    "deploy_hook": os.environ.get("DEPLOY_HOOK"),
    "claude_model": os.environ.get("CLAUDE_MODEL") or "claude-2",
    "anthropic_key": os.environ.get("ANTHROPIC_API_KEY"),
    "owner_id": os.environ.get("OWNER_ID"),
    "token": os.environ.get("DISCORD_TOKEN"),
    "db_name": os.environ.get("DB_NAME"),
    "db_user": os.environ.get("DB_USER"),
    "db_pass": os.environ.get("DB_PASS"),
    "db_url": os.environ.get("DATABASE_URL")
}

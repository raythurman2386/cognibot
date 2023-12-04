import os
import discord
from dotenv import load_dotenv
from db.database import add_user_to_table, init_db, is_user_in_table
from utils.logger import app_logger
from utils.env import env_vars


load_dotenv()
bot = discord.Bot(intents=discord.Intents.all())
owner_id = env_vars["owner_id"]
token = env_vars["token"]


cogs_list = ["greetings", "moderation", "openai", "anthropic"]
for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


@bot.event
async def on_ready():
    app_logger.info(f"{bot.user} is ready and online!")
    print(f"{bot.user} is ready and online!")
    init_db()
    owner_id_str = str(owner_id)
    for table in ["authorized_users", "moderators"]:
        if not is_user_in_table(owner_id_str, table):
            add_user_to_table(owner_id_str, table)


if __name__ == "__main__":
    app_logger.info("Script started")
    try:
        bot.run(token)
    except Exception as e:
        app_logger.exception("An unexpected error occurred")
    app_logger.info("Script ended")

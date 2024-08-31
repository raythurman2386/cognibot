import asyncio
import discord
from dotenv import load_dotenv
from db.database import add_user_to_table, init_db, is_user_in_table
from utils.logger import app_logger
from utils.env import env_vars

load_dotenv()
owner_id = env_vars["owner_id"]
token = env_vars["token"]


class Cognibot(discord.Bot):
    async def on_ready(self):
        app_logger.info(f"{self.user} is ready and online!")
        print(f"{self.user} is ready and online!")
        init_db()
        owner_id_str = str(owner_id)
        for table in ["moderators"]:
            if not is_user_in_table(owner_id_str, table):
                add_user_to_table(owner_id_str, table)

    async def on_disconnect(self):
        app_logger.warning("Bot disconnected from Discord")

    async def on_connect(self):
        app_logger.info("Bot reconnected to Discord")

    async def on_resumed(self):
        app_logger.info("Bot session resumed")


bot = Cognibot(intents=discord.Intents.all())

cogs_list = ["greetings", "moderation", "openai", "fun", "anthropic"]
for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


async def main():
    app_logger.info("Script started")
    try:
        await bot.start(token)
    except discord.LoginFailure:
        app_logger.error("Failed to log in: Invalid token")
    except discord.HTTPException as e:
        app_logger.error(f"HTTP request failed: {e}")
    except Exception as e:
        app_logger.exception(f"An unexpected error occurred: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()
        app_logger.info("Script ended")


if __name__ == "__main__":
    asyncio.run(main())

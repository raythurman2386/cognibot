import asyncio
from collections import deque
from datetime import datetime
import discord
import psutil
from discord.ext import tasks, commands
from dotenv import load_dotenv
from db.database import ChatDatabase
from utils.logger import app_logger
from utils.env import env_vars

load_dotenv()
token = env_vars["token"]


class Cognibot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = ChatDatabase()
        self.command_usage = {}
        self.uptime_start = datetime.now()
        self.error_log = deque(maxlen=100)

    async def on_ready(self):
        app_logger.info(f"{self.user} is ready and online!")
        self.monitor_health.start()
        self.db.init_db()

    async def on_disconnect(self):
        app_logger.warning("Bot disconnected from Discord")

    async def on_connect(self):
        app_logger.info("Bot reconnected to Discord")

    async def on_resumed(self):
        app_logger.info("Bot session resumed")
    
    @tasks.loop(hours=1)
    async def monitor_health(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent
        app_logger.info(
            f"CPU usage: {cpu_usage}%, Memory usage: {memory_usage}%, Disk usage: {disk_usage}%"
        )

        if cpu_usage > 90 or memory_usage > 90 or disk_usage > 90:
            app_logger.warning(
                f"High resource usage detected: CPU {cpu_usage}%, Memory {memory_usage}%, Disk {disk_usage}%"
            )

    async def on_command_error(self, ctx, error):
        self.error_log.append((datetime.now(), str(error)))
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds."
            )
        else:
            await ctx.send("An error occurred. Please try again later.")
        app_logger.error(f"Command error in {ctx.command}: {str(error)}")

    async def on_command_completion(self, ctx):
        command_name = ctx.command.name
        self.command_usage[command_name] = self.command_usage.get(command_name, 0) + 1


bot = Cognibot(intents=discord.Intents.all())

cogs_list = ["greetings", "openai", "fun", "anthropic"]
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

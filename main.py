import discord
import os
from dotenv import load_dotenv
from db.database import add_user_to_table, init_db, is_user_in_table


load_dotenv()
bot = discord.Bot(intents=discord.Intents.all())
owner_id = os.environ.get("OWNER_ID")
allowed_channel_id = os.environ.get("ALLOWED_CHANNEL_ID")


cogs_list = ["greetings", "moderation", "openai"]
for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    init_db()
    owner_id_str = str(owner_id)
    for table in ["authorized_users", "moderators"]:
        if not is_user_in_table(owner_id_str, table):
            add_user_to_table(owner_id_str, table)


@bot.event
async def on_message(message: discord.Message):
    if str(message.channel.id) == allowed_channel_id and is_user_in_table(
        str(message.author.id), "authorized_users"
    ):
        await bot.process_commands(message)


token = os.environ.get("DISCORD_TOKEN")
bot.run(token)

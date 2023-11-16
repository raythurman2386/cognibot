import discord
import os
from dotenv import load_dotenv
from db.database import add_user_to_table, init_db, is_user_in_table

from utils.openai import askgpt, imgGeneration

load_dotenv()
bot = discord.Bot(intents=discord.Intents.all())
owner_id = os.environ.get("OWNER_ID")
allowed_channel_id = os.environ.get("ALLOWED_CHANNEL_ID")


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    init_db()
    owner_id_str = str(owner_id)
    for table in ["authorized_users", "moderators"]:
        if not is_user_in_table(owner_id_str, table):
            add_user_to_table(owner_id_str, table)


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.slash_command(name="chatgpt", description="Send a promt to ChatGPT")
async def chat_gpt(ctx):
    print(ctx.message)
    answer = askgpt(ctx.message)
    await ctx.respond(answer)


@bot.slash_command(
    name="dalle", description="Generate an image from a prompt with Dall-E-3"
)
async def ai_image(ctx):
    print(ctx.message)
    image_url = imgGeneration(ctx.message)
    await ctx.respond(image_url)


token = os.environ.get("DISCORD_TOKEN")
bot.run(token)

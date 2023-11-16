import discord
import os
from dotenv import load_dotenv
from db.backup import backup_database
from db.database import add_user_to_table, init_db, is_user_in_table

from utils.openai import askgpt, imgGeneration
from utils.utils import send_large_message

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


@bot.event
async def on_message(message: discord.Message):
    if str(message.channel.id) == allowed_channel_id and is_user_in_table(
        str(message.author.id), "authorized_users"
    ):
        await bot.process_commands(message)


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.slash_command(
    name="chatgpt",
    description="Send a promt to ChatGPT",
    aliases=["aiimg", "img"],
)
async def chat_gpt(ctx, prompt: str):
    await ctx.defer(ephemeral=True)
    answer = askgpt(prompt)
    await send_large_message(ctx, answer)


@bot.slash_command(
    name="dalle", description="Generate an image from a prompt with Dall-E-3"
)
async def ai_image(ctx, prompt: str):
    await ctx.defer(ephemeral=True)
    image_url = imgGeneration(prompt)
    await send_large_message(ctx, image_url)


@bot.slash_command(
    name="auth",
    description="A moderator is able to add a user to the authorized gpt users table.",
    help="A moderator is able to add a user to the authorized gpt users table.",
    aliases=[],
    hidden=True,
)
async def auth(ctx, member: discord.Member):
    await ctx.defer(ephemeral=True)
    if is_user_in_table(str(ctx.author.id), "moderators"):
        user_id = str(member.id)
        if not is_user_in_table(user_id, "authorized_users"):
            add_user_to_table(user_id, "authorized_users")
            await ctx.followup.send(f"{member} added to authorized users")
        else:
            await ctx.followup.send(f"{member} already authorized")
    else:
        await ctx.followup.send("You are not authorized for moderation commands")


@bot.slash_command(
    name="addmod",
    description="A moderator is able to add a user to the moderators users table.",
    help="A moderator is able to add a user to the moderators users table.",
    aliases=["newmod"],
    hidden=True,
)
async def addmod(ctx, member: discord.Member):
    await ctx.defer(ephemeral=True)
    if is_user_in_table(str(ctx.author.id), "moderators"):
        user_id = str(member.id)
        if not is_user_in_table(user_id, "moderators"):
            add_user_to_table(user_id, "moderators")
            await ctx.followup.send(f"{member} added to moderators")
        else:
            await ctx.followup.send(f"{member} already a moderator")
    else:
        await ctx.followup.send("You are not authorized for moderation commands")


# Backup Database
@bot.slash_command(
    name="backup",
    description="A moderator is able to backup the chat log to the server.",
    help="A moderator is able to backup the chat log to the server.",
    aliases=[],
    hidden=True,
)
async def backup(ctx):
    await ctx.defer(ephemeral=True)
    if is_user_in_table(str(ctx.author.id), "moderators"):
        base_dir = os.getcwd()
        db_path = f"{base_dir}/chat_log.db"
        backup_folder = f"{base_dir}/backups/"
        backup_database(db_path, backup_folder)
        await ctx.followup.send("Database successfully backed up!")
    else:
        await ctx.followup.send("You are not authorized for moderation commands")


token = os.environ.get("DISCORD_TOKEN")
bot.run(token)

import os
import discord
from discord.ext import commands
from db.database import is_user_in_table

from utils.openai import ask_gpt, img_generation
from utils.utils import send_large_message


class Openai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_channel_id = os.environ.get("ALLOWED_CHANNEL_ID")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot:
            return

        if not is_user_in_table(message.author.id, "authorized_users"):
            return

        if not message.channel.id == self.allowed_channel_id:
            return

    @discord.slash_command(
        name="chatgpt",
        description="Send a prompt to ChatGPT",
    )
    async def chat_gpt(self, ctx, prompt):
        if is_user_in_table(prompt.author.id, "authorized_users"):
            await ctx.defer(ephemeral=True)
            answer = ask_gpt(prompt)
            await send_large_message(ctx, answer)
        else:
            await ctx.followup.send(
                "You are not authorized to use ChatGPT at this time."
            )

    @discord.slash_command(
        name="dalle",
        description="Send a prompt to Dall E 3",
    )
    async def dall_e(self, ctx, prompt):
        if is_user_in_table(prompt.author.id, "authorized_users"):
            await ctx.defer(ephemeral=True)
            image_url = img_generation(prompt)
            await send_large_message(ctx, image_url)
        else:
            await ctx.followup.send(
                "You are not authorized to use DALL E 3 at this time."
            )


def setup(bot):
    bot.add_cog(Openai(bot))

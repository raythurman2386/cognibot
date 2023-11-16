import discord
from discord.ext import commands

from utils.openai import ask_gpt, img_generation
from utils.utils import send_large_message


class Openai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="chatgpt",
        description="Send a prompt to ChatGPT",
    )
    async def chat_gpt(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        answer = ask_gpt(prompt)
        await send_large_message(ctx, answer)

    @discord.slash_command(
        name="dalle",
        description="Send a prompt to Dall E 3",
    )
    async def dall_e(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        image_url = img_generation(prompt)
        await send_large_message(ctx, image_url)


def setup(bot):
    bot.add_cog(Openai(bot))

import discord
from discord.ext import commands

from utils.openai import askgpt, imgGeneration
from utils.utils import send_large_message


class Openai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="chatgpt",
        description="Send a prompt to ChatGPT",
    )
    async def chatgpt(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        answer = askgpt(prompt)
        await send_large_message(ctx, answer)

    @discord.slash_command(
        name="dalle",
        description="Send a prompt to Dall E 3",
    )
    async def dalle(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        image_url = imgGeneration(prompt)
        await send_large_message(ctx, image_url)


def setup(bot):
    bot.add_cog(Openai(bot))

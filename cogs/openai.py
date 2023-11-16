import discord
from discord.ext import commands

from utils.openai import askgpt, imgGeneration
from utils.utils import send_large_message


class Openai(
    commands.Cog
):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(
        self, bot
    ):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @discord.slash_command(
        name="chatgpt",
        description="Send a promt to ChatGPT",
    )
    async def chatgpt(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        answer = askgpt(prompt)
        await send_large_message(ctx, answer)

    @discord.slash_command(
        name="dalle",
        description="Send a promt to Dall E 3",
    )
    async def dalle(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        image_url = imgGeneration(prompt)
        await send_large_message(ctx, image_url)


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Openai(bot))  # add the cog to the bot

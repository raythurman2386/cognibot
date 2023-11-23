import os
import discord
from discord.ext import commands
from db.database import is_user_in_table

from utils.openai import ask_claude
from utils.utils import send_large_message


class Anthropic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_channel_id = os.environ.get("ALLOWED_CHANNEL_ID")

    @discord.slash_command(
        name="claude",
        description="Send a prompt to Anthropic's Claude-2 API",
    )
    async def claude(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        if is_user_in_table(str(ctx.author.id), "authorized_users"):
            answer = ask_claude(prompt)
            await send_large_message(ctx, answer)
        else:
            await ctx.followup.send("You are not authorized for GPT commands")


def setup(bot):
    bot.add_cog(Anthropic(bot))

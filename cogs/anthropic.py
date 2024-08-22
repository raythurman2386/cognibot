import discord
from discord.ext import commands
from db.database import is_user_in_table

from utils.anthropic import ask_claude
from utils.utils import send_large_message


class Anthropic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="claude",
        description="Send a prompt to Anthropic's Claude-2 API",
    )
    async def claude(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        try:
            if is_user_in_table(str(ctx.author.id), "authorized_users"):
                answer = ask_claude(prompt)
                await send_large_message(ctx, answer)
            else:
                await ctx.followup.send("You are not authorized for GPT commands")
        except:
            await ctx.followup.send("❌ An error occurred. Please try again later.")


def setup(bot):
    bot.add_cog(Anthropic(bot))

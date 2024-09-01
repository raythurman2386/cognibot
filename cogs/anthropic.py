import discord
from discord.ext import commands
from db.database import ChatDatabase
from utils.anthropic import ask_claude
from utils.utils import send_large_message


class Anthropic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = ChatDatabase()

    @discord.slash_command(
        name="claude",
        description="Send a prompt to Anthropic's Claude-2 API",
    )
    async def claude(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        try:
            user_id = str(ctx.author.id)
            answer = ask_claude(user_id, prompt, self.db)
            await send_large_message(ctx, answer)
        except Exception as e:
            await ctx.followup.send(f"❌ An error occurred: {str(e)}")

    @discord.slash_command(
        name="clear_chat",
        description="Clear your chat history",
    )
    async def clear_chat(self, ctx):
        user_id = str(ctx.author.id)
        self.db.clear_user_chat_log(user_id)
        await ctx.respond("Your chat history has been cleared.", ephemeral=True)


def setup(bot):
    bot.add_cog(Anthropic(bot))

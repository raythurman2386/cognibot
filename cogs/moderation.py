import os
import discord
from discord.ext import commands
from db.backup import backup_database
from db.database import add_user_to_table, is_user_in_table


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_channel_id = os.environ.get("ALLOWED_CHANNEL_ID")

    @discord.slash_command(
        name="addmod",
        description="Add moderator for Bot",
    )
    async def add_mod(self, ctx, member: discord.Member):
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

    @discord.slash_command(
        name="backup",
        description="A moderator is able to backup the chat log to the server.",
        help="A moderator is able to backup the chat log to the server.",
        aliases=[],
        hidden=True,
    )
    async def backup(self, ctx):
        await ctx.defer(ephemeral=True)
        if is_user_in_table(str(ctx.author.id), "moderators"):
            base_dir = os.getcwd()
            db_path = f"{base_dir}/db/chat_log.db"
            backup_folder = f"{base_dir}/Backups/"
            backup_database(db_path, backup_folder)
            await ctx.followup.send("Database successfully backed up!")
        else:
            await ctx.followup.send("You are not authorized for moderation commands")


def setup(bot):
    bot.add_cog(Moderation(bot))

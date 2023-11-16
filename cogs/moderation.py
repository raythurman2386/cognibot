import os
import discord
from discord.ext import commands
from db.backup import backup_database
from db.database import add_user_to_table, is_user_in_table


class Moderation(
    commands.Cog
):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(
        self, bot
    ):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @discord.slash_command(
        name="auth",
        description="Authorize user to use chat gpt",
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

    @discord.slash_command(
        name="addmod",
        description="Add moderator for Bot",
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
    @discord.slash_command(
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


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Moderation(bot))  # add the cog to the bot

import discord
from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.defer(ephemeral=True)
        await ctx.followup.send("Hello!")

    @discord.slash_command()
    async def goodbye(self, ctx):
        await ctx.defer(ephemeral=True)
        await ctx.followup.send("Goodbye!")

    @discord.user_command()
    async def greet(self, ctx, member: discord.Member):
        await ctx.defer(ephemeral=True)
        await member.send(f"{ctx.author.mention} says hello to {member.mention}!")
        await ctx.followup.send(f"PM Sent to {member}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(
            f"""Welcome to the server, {member.mention}! 👋

We're so glad you decided to join us. Please take a moment to review the #welcome-and-rules channel to get started.

If you have any questions, feel free to ask one of our moderators.

We hope you enjoy your time here! Don't hesitate to introduce yourself in #introductions once you're settled in.

- The Ravenwood Team"""
        )


def setup(bot):
    bot.add_cog(Greetings(bot)) 

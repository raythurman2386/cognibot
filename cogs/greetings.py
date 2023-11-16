import discord
from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

    @discord.slash_command()
    async def goodbye(self, ctx):
        await ctx.respond("Goodbye!")

    @discord.user_command()
    async def greet(self, ctx, member: discord.Member):
        await ctx.respond(f"{ctx.author.mention} says hello to {member.mention}!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send("Welcome to the server!")


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Greetings(bot))  # add the cog to the bot

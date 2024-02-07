import pytest
import discord
from discord.ext import commands

@pytest.fixture
def bot():
    bot = discord.Bot()
    # Set up any necessary bot configuration here
    return bot

@bot.slash_command()
async def ping(ctx):
    await ctx.send("Pong!")

async def test_ping(bot):
    async def mock_send(message):
        assert message == "Pong!"
    bot.add_command(mock_send)  # Override the real ping command
    await bot.process_commands(message=commands.Message(content="/ping"))
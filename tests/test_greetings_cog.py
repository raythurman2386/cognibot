import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord.ext import commands
from cogs.greetings import Greetings  # adjust this import as needed


@pytest.fixture
def bot():
    return MagicMock(spec=commands.Bot)


@pytest.fixture
def cog(bot):
    return Greetings(bot)


@pytest.mark.asyncio
async def test_hello(cog):
    ctx = AsyncMock()
    # Access the callback of the slash command
    await cog.hello.callback(cog, ctx)
    ctx.defer.assert_called_once_with(ephemeral=True)
    ctx.followup.send.assert_called_once_with("Hello!")


@pytest.mark.asyncio
async def test_goodbye(cog):
    ctx = AsyncMock()
    # Access the callback of the slash command
    await cog.goodbye.callback(cog, ctx)
    ctx.defer.assert_called_once_with(ephemeral=True)
    ctx.followup.send.assert_called_once_with("Goodbye!")


@pytest.mark.asyncio
async def test_greet(cog):
    ctx = AsyncMock()
    member = AsyncMock(spec=discord.Member)
    member.mention = "@user"
    ctx.author.mention = "@author"

    # Mock the send method to return a coroutine
    member.send = AsyncMock()

    # Access the callback of the user command
    await cog.greet.callback(cog, ctx, member)

    ctx.defer.assert_called_once_with(ephemeral=True)
    member.send.assert_called_once_with("@author says hello to @user!")
    ctx.followup.send.assert_called_once_with(f"PM Sent to {member}")


@pytest.mark.asyncio
async def test_on_member_join(cog):
    member = AsyncMock()
    member.id = 12345
    member.mention = "@newuser"
    member.send = AsyncMock()

    with patch.object(
        cog.db, "create_user_settings", return_value=None
    ) as mock_create_user_settings:
        await cog.on_member_join(member)
        mock_create_user_settings.assert_called_once_with(12345)
        member.send.assert_called_once()

        welcome_message = f"""Welcome to the server, {member.mention}! 👋

We're so glad you decided to join us. Please take a moment to review the #welcome-and-rules channel to get started.

If you have any questions, feel free to ask one of our moderators.

We hope you enjoy your time here! Don't hesitate to introduce yourself in #introductions once you're settled in.

- The Ravenwood Team"""
        member.send.assert_called_once_with(welcome_message)
        assert "@newuser" in member.send.call_args[0][0]

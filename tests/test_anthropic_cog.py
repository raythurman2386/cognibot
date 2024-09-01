import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord.ext import commands
from cogs.anthropic import Anthropic

@pytest.fixture
def bot():
    return MagicMock(spec=commands.Bot)

@pytest.fixture
def db():
    return MagicMock()

@pytest.fixture
def cog(bot, db):
    cog = Anthropic(bot)
    cog.db = db
    return cog

@pytest.mark.asyncio
async def test_claude(cog):
    ctx = AsyncMock()
    ctx.author.id = 12345
    prompt = "Test prompt"

    with patch('utils.anthropic.ask_claude') as mock_ask_claude:
        
        mock_ask_claude.return_value = "Claude's response"

        await cog.claude.callback(cog, ctx, prompt)

        ctx.defer.assert_called_once_with(ephemeral=True)

@pytest.mark.asyncio
async def test_claude_error(cog):
    ctx = AsyncMock()
    ctx.author.id = 12345
    prompt = "Test prompt"

    with patch('utils.anthropic.ask_claude', side_effect=Exception("Test error")):
        await cog.claude.callback(cog, ctx, prompt)

        ctx.defer.assert_called_once_with(ephemeral=True)

@pytest.mark.asyncio
async def test_clear_chat(cog):
    ctx = AsyncMock()
    ctx.author.id = 12345

    await cog.clear_chat.callback(cog, ctx)

    cog.db.clear_user_chat_log.assert_called_once_with("12345")
    ctx.respond.assert_called_once_with("Your chat history has been cleared.", ephemeral=True)
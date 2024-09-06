import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord.ext import commands
from cogs.anthropic import Anthropic
from utils.utils import CustomError


@pytest.fixture
def bot():
    return MagicMock(spec=commands.Bot)


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def anthropic_client():
    return MagicMock()


@pytest.fixture
def cog(bot, db, anthropic_client):
    with patch("cogs.anthropic.AnthropicClient", return_value=anthropic_client):
        cog = Anthropic(bot)
        cog.db = db
        return cog


@pytest.mark.asyncio
async def test_claude(cog):
    ctx = AsyncMock()
    ctx.author.id = 12345
    prompt = "Test prompt"

    cog._ask_claude = MagicMock(return_value="Claude's response")

    with patch("cogs.anthropic.send_large_message") as mock_send_large_message:
        await cog.claude.callback(cog, ctx, prompt)

        ctx.defer.assert_called_once_with(ephemeral=True)
        cog._ask_claude.assert_called_once_with("12345", prompt)


@pytest.mark.asyncio
async def test_claude_error(cog):
    ctx = AsyncMock()
    ctx.author.id = 12345
    prompt = "Test prompt"

    cog._ask_claude = MagicMock(side_effect=Exception("Test error"))

    await cog.claude.callback(cog, ctx, prompt)

    ctx.defer.assert_called_once_with(ephemeral=True)
    ctx.followup.send.assert_called_once_with("❌ An error occurred: Test error")


@pytest.mark.asyncio
async def test_clear_chat(cog):
    ctx = AsyncMock()
    ctx.author.id = 12345

    await cog.clear_chat.callback(cog, ctx)

    cog.db.clear_user_chat_log.assert_called_once_with("12345")
    ctx.respond.assert_called_once_with(
        "Your chat history has been cleared.", ephemeral=True
    )


@pytest.mark.asyncio
async def test_ask_claude_error(cog):
    user_id = "12345"
    question = "Test question"

    cog.db.get_chat_log.side_effect = Exception("Database error")

    result = cog._ask_claude(user_id, question)
    assert "An error occurred" in result


@pytest.mark.asyncio
async def test_ask_claude_empty_question(cog):
    user_id = "12345"
    question = ""

    result = cog._ask_claude(user_id, question)
    assert "Please provide a question for Claude!" in result

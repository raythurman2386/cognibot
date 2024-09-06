import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord.ext import commands
from cogs.openai import OpenAI


@pytest.fixture
def bot():
    return MagicMock(spec=commands.Bot)


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def openai_client():
    return MagicMock()


@pytest.fixture
def cog(bot, db, openai_client):
    with patch("openai.OpenAI", return_value=openai_client):
        cog = OpenAI(bot)
        cog.db = db
        cog.client = openai_client
        return cog


@pytest.mark.asyncio
async def test_chat_gpt_error(cog):
    ctx = AsyncMock()
    ctx.author.id = 12345
    prompt = "Test prompt"

    cog._ask_gpt = MagicMock(side_effect=Exception("Test error"))

    await cog.chat_gpt.callback(cog, ctx, prompt)

    ctx.defer.assert_called_once_with(ephemeral=True)
    ctx.followup.send.assert_called_once_with("❌ An error occurred: Test error")


def test_ask_gpt_empty_question(cog):
    user_id = "12345"
    question = ""

    result = cog._ask_gpt(user_id, question)
    assert "An error occurred" in result

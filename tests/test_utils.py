import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord.ext import commands
from utils.utils import (
    get_user_id,
    format_response,
    send_large_message,
)

@pytest.mark.asyncio
async def test_get_user_id():
    ctx = AsyncMock()
    member = MagicMock()
    member.name = "test_user"
    member.id = "12345"
    ctx.guild.members = [member]
    
    result = await get_user_id(ctx, "test_user")
    assert result == "12345"
    
    result = await get_user_id(ctx, "nonexistent_user")
    assert result is None

@pytest.mark.asyncio
async def test_format_response():
    response = "This is a test response"
    formatted = await format_response(response)
    assert formatted == "This is a test response"
    
    response = 12345
    formatted = await format_response(response)
    assert formatted == "12345"

@pytest.mark.asyncio
async def test_send_large_message():
    ctx = AsyncMock()
    ctx.response.is_done.return_value = False
    
    # Test with a short message
    await send_large_message(ctx, "Short message")
    ctx.followup.send.assert_called_once_with("Short message", ephemeral=True)
    
    # Reset mock
    ctx.reset_mock()
    
    # Test with a long message
    long_message = "a" * 3000
    await send_large_message(ctx, long_message)
    assert ctx.followup.send.call_count == 2
    ctx.followup.send.assert_any_call("a" * 2000, ephemeral=True)
    ctx.followup.send.assert_any_call("a" * 1000, ephemeral=True)
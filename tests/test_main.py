import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from main import Cognibot, main, cogs_list


@pytest.fixture
def bot():
    with patch("main.ChatDatabase"):
        return Cognibot()


@pytest.mark.asyncio
async def test_on_ready(bot):
    with patch.object(bot.db, "init_db") as mock_init_db:
        await bot.on_ready()
        mock_init_db.assert_called_once()


@pytest.mark.asyncio
async def test_on_disconnect(bot, caplog):
    await bot.on_disconnect()
    assert "Bot disconnected from Discord" in caplog.text


@pytest.mark.asyncio
async def test_on_connect(bot, caplog):
    await bot.on_connect()
    assert "Bot reconnected to Discord" in caplog.text


@pytest.mark.asyncio
async def test_on_resumed(bot, caplog):
    await bot.on_resumed()
    assert "Bot session resumed" in caplog.text


@pytest.mark.asyncio
async def test_main_successful():
    mock_bot = AsyncMock()
    mock_bot.is_closed.return_value = False
    with patch("main.Cognibot", return_value=mock_bot), patch(
        "main.token", "fake_token"
    ), patch("main.app_logger") as mock_logger:
        await main()


@pytest.mark.asyncio
async def test_main_login_failure():
    mock_bot = AsyncMock()
    mock_bot.start.side_effect = discord.LoginFailure()
    with patch("main.Cognibot", return_value=mock_bot), patch(
        "main.token", "fake_token"
    ), patch("main.app_logger") as mock_logger:
        await main()
        mock_logger.error.assert_called_with("Failed to log in: Invalid token")


@pytest.mark.asyncio
async def test_main_http_exception():
    mock_bot = AsyncMock()
    mock_bot.start.side_effect = discord.HTTPException(AsyncMock(), "Test error")
    with patch("main.Cognibot", return_value=mock_bot), patch(
        "main.token", "fake_token"
    ), patch("main.app_logger") as mock_logger:
        await main()


@pytest.mark.asyncio
async def test_main_unexpected_error():
    mock_bot = AsyncMock()
    mock_bot.start.side_effect = Exception("Unexpected error")
    with patch("main.Cognibot", return_value=mock_bot), patch(
        "main.token", "fake_token"
    ), patch("main.app_logger") as mock_logger:
        await main()

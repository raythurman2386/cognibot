import pytest
from unittest.mock import AsyncMock, patch
import discord
from discord.ext import commands
from cogs.fun import Fun


@pytest.fixture
def bot():
    return AsyncMock(spec=commands.Bot)


@pytest.fixture
def cog(bot):
    return Fun(bot)


@pytest.mark.asyncio
async def test_roll_dice_valid(cog):
    ctx = AsyncMock()
    with patch("random.randint", return_value=4):
        await cog.roll_dice.callback(cog, ctx, "d6")
    ctx.respond.assert_called_once_with("🎲 You rolled a d6 and got a 4!")


@pytest.mark.asyncio
async def test_roll_dice_invalid_format(cog):
    ctx = AsyncMock()
    await cog.roll_dice.callback(cog, ctx, "invalid")
    ctx.respond.assert_called_once_with(
        "❌ Invalid dice format. Use the format 'dN', where N is a number (e.g., d6, d20)."
    )


@pytest.mark.asyncio
async def test_roll_dice_negative_sides(cog):
    ctx = AsyncMock()
    await cog.roll_dice.callback(cog, ctx, "d-6")
    ctx.respond.assert_called_once_with(
        "❌ Invalid dice format. Use the format 'dN', where N is a number (e.g., d6, d20)."
    )


@pytest.mark.asyncio
async def test_roll_dice_zero_sides(cog):
    ctx = AsyncMock()
    await cog.roll_dice.callback(cog, ctx, "d0")
    ctx.respond.assert_called_once_with(
        "❌ The number of sides must be a positive integer."
    )


@pytest.mark.asyncio
async def test_roll_dice_exception(cog):
    ctx = AsyncMock()
    with patch("random.randint", side_effect=Exception("Test exception")):
        await cog.roll_dice.callback(cog, ctx, "d6")
    ctx.respond.assert_called_once_with("❌ An error occurred. Please try again later.")


@pytest.mark.asyncio
async def test_flip_coin(cog):
    ctx = AsyncMock()
    with patch("random.choice", return_value="Heads"):
        await cog.flip_coin.callback(cog, ctx)
    ctx.respond.assert_called_once_with("🪙 The coin landed on Heads!")


@pytest.mark.asyncio
async def test_flip_coin_exception(cog):
    ctx = AsyncMock()
    with patch("random.choice", side_effect=Exception("Test exception")):
        await cog.flip_coin.callback(cog, ctx)
    ctx.respond.assert_called_once_with("❌ An error occurred. Please try again later.")

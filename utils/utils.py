import discord
from discord.ext import commands
from utils.logger import app_logger


async def get_user_id(ctx: commands.Context, username: str) -> str:
    member = discord.utils.find(lambda m: m.name == username, ctx.guild.members)
    return member.id if member else None


async def format_response(response):
    """This function will be used to take the response from chat gpt and format it for Discord."""
    # Convert response to a string if it's not already
    response = str(response)

    # Discord uses markdown for formatting, I'm testing different system prompts to return the response in advance before implementing this fully
    formatted_response = f"{response}"

    return formatted_response


async def send_large_message(ctx: commands.Context, response: str):
    try:
        chunks = [response[i : i + 2000] for i in range(0, len(response), 2000)]

        if not ctx.response.is_done():
            await ctx.defer(ephemeral=True)
        for chunk in chunks:
            await ctx.followup.send(chunk, ephemeral=True)
    except discord.errors.HTTPException:
        await ctx.followup.send(
            "The response is too large to display. Please try with a shorter prompt."
        )


class CustomError(Exception):
    pass


def handle_error(e):
    if isinstance(e, CustomError):
        app_logger.warning(f"There has been an error: {e}")
        return str(e)
    else:
        app_logger.error(f"There has been an error: {e}")
        return "Blimey! Something went wrong: " + str(e)

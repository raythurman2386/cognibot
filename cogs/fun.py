import discord
import random
from discord.ext import commands
from utils.logger import app_logger


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="roll_dice",
        description="Roll a dice of a specified type (e.g., d6, d20)",
    )
    async def roll_dice(self, ctx, dice: str):
        try:
            if not dice.startswith("d") or not dice[1:].isdigit().lower():
                await ctx.respond(
                    "❌ Invalid dice format. Use the format 'dN', where N is a number (e.g., d6, d20)."
                )
                app_logger.warn(
                    "❌ Invalid dice format. Use the format 'dN', where N is a number (e.g., d6, d20)."
                )
                return

            sides = int(dice[1:])
            if sides <= 0:
                await ctx.respond("❌ The number of sides must be a positive integer.")
                app_logger.warn("❌ The number of sides must be a positive integer.")
                return

            result = random.randint(1, sides)
            await ctx.respond(f"🎲 You rolled a {dice} and got a {result}!")
            app_logger.info(f"🎲 You rolled a {dice} and got a {result}!")
            return

        except Exception as e:
            await ctx.respond("❌ An error occurred. Please try again later.")
            app_logger.error(f"Error in roll_dice: {e}")

    @discord.slash_command(
        name="flip_coin",
        description="Flip a coin and get heads or tails",
    )
    async def flip_coin(self, ctx):
        try:
            result = random.choice(["Heads", "Tails"])
            await ctx.respond(f"🪙 The coin landed on {result}!")

        except Exception as e:
            await ctx.respond("❌ An error occurred. Please try again later.")
            app_logger.error(f"Error in flip_coin: {e}")


def setup(bot):
    bot.add_cog(Fun(bot))

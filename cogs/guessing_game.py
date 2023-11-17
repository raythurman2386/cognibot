import discord
from discord.ext import commands
import random


class GuessingGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guess", help="Play the number guessing game!")
    async def play_guessing_game(self, ctx):
        await ctx.send(
            "Welcome to the Number Guessing Game! I've selected a number between 1 and 100. Try to guess it!"
        )

        number_to_guess = random.randint(1, 100)
        attempts = 0

        while True:
            try:
                guess = await self.bot.wait_for(
                    "message",
                    timeout=30.0,
                    check=lambda m: m.author == ctx.author and m.content.isdigit(),
                )
                guess = int(guess.content)

                attempts += 1

                if guess == number_to_guess:
                    await ctx.send(
                        f"Congratulations! You've guessed the correct number {number_to_guess} in {attempts} attempts."
                    )
                    break
                elif guess < number_to_guess:
                    await ctx.send("Too low! Try again.")
                else:
                    await ctx.send("Too high! Try again.")

            except TimeoutError:
                await ctx.send(
                    f"Time's up! The game has ended. The correct number was {number_to_guess}."
                )
                break


def setup(bot):
    bot.add_cog(GuessingGame(bot))

import os
import discord
import random
import requests
import html
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="roll_dice",
        description="Roll a dice of a specified type (e.g., d6, d20)",
    )
    async def roll_dice(self, ctx, dice: str):
        # Validate dice format
        if not dice.startswith('d') or not dice[1:].isdigit():
            await ctx.respond("❌ Invalid dice format. Use the format 'dN', where N is a number (e.g., d6, d20).")
            return

        # Extract the number of sides
        sides = int(dice[1:])
        if sides <= 0:
            await ctx.respond("❌ The number of sides must be a positive integer.")
            return

        # Roll the dice
        result = random.randint(1, sides)
        await ctx.respond(f"🎲 You rolled a {dice} and got a {result}!")

    @discord.slash_command(
        name="flip_coin",
        description="Flip a coin and get heads or tails",
    )
    async def flip_coin(self, ctx):
        result = random.choice(["Heads", "Tails"])
        await ctx.respond(f"🪙 The coin landed on {result}!")

    @discord.slash_command(
        name="trivia",
        description="Answer a random trivia question",
    )
    async def trivia(self, ctx):
        # Fetch a trivia question from Open Trivia Database API
        url = "https://opentdb.com/api.php?amount=1&type=multiple"
        response = requests.get(url)
        data = response.json()

        if data["response_code"] == 0:
            question_data = data["results"][0]
            question = html.unescape(question_data["question"])
            correct_answer = html.unescape(question_data["correct_answer"])
            all_answers = question_data["incorrect_answers"]
            all_answers.append(correct_answer)
            random.shuffle(all_answers)
            formatted_answers = "\n".join([f"{idx + 1}. {html.unescape(ans)}" for idx, ans in enumerate(all_answers)])

            await ctx.send(f"❓ {question}\n\n{formatted_answers}")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await self.bot.wait_for('message', check=check, timeout=30.0)
                answer_index = int(response.content.strip()) - 1
                if all_answers[answer_index].lower() == correct_answer.lower():
                    await ctx.send("🎉 Correct!")
                else:
                    await ctx.send(f"❌ Incorrect. The correct answer was **{correct_answer}** .")
            except (asyncio.TimeoutError, ValueError, IndexError):
                await ctx.send(f"⏰ Time's up! The correct answer was **{correct_answer}** .")
        else:
            await ctx.send("⚠️ Failed to fetch trivia question. Please try again later.")

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Fun(bot))  # add the cog to the bot

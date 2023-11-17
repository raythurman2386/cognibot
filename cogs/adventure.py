import discord
from discord.ext import commands


class AdventureGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="adventure", help="Embark on a text adventure!")
    async def play_adventure_game(self, ctx):
        await ctx.send(
            "Welcome to the Text Adventure Game! You find yourself in a mysterious land with multiple paths."
        )

        choices = {"1": "Take the left path.", "2": "Take the right path."}

        current_scene = "start"

        while True:
            await ctx.send(
                f"\n**{choices[current_scene]}**\n(Type the number corresponding to your choice)"
            )

            choice = await self.bot.wait_for(
                "message",
                timeout=30.0,
                check=lambda m: m.author == ctx.author
                and m.content.isdigit()
                and m.content in choices,
            )

            if current_scene == "start":
                if choice.content == "1":
                    await ctx.send(
                        "You encounter a friendly merchant. He offers you a map."
                    )
                    current_scene = "map"
                elif choice.content == "2":
                    await ctx.send(
                        "You hear mysterious sounds coming from the right path. It seems dangerous."
                    )
                    current_scene = "danger"

            elif current_scene == "map":
                if choice.content == "1":
                    await ctx.send(
                        "You decide to follow the map. The path leads you to a hidden treasure!"
                    )
                    break
                elif choice.content == "2":
                    await ctx.send(
                        "You ignore the map and continue your journey. The path becomes darker."
                    )
                    current_scene = "dark_path"

            elif current_scene == "danger":
                if choice.content == "1":
                    await ctx.send(
                        "You cautiously proceed. It was just a flock of birds."
                    )
                    current_scene = "start"
                elif choice.content == "2":
                    await ctx.send("You decide to turn back and take the left path.")
                    current_scene = "start"

            elif current_scene == "dark_path":
                if choice.content == "1":
                    await ctx.send(
                        "You encounter a mysterious figure. They give you a riddle."
                    )
                    current_scene = "riddle"
                elif choice.content == "2":
                    await ctx.send(
                        "You use a torch to light up the path. You discover a hidden passage."
                    )
                    current_scene = "hidden_passage"

            elif current_scene == "riddle":
                if choice.content == "1":
                    await ctx.send(
                        "You solve the riddle and gain the figure's trust. They guide you to safety."
                    )
                    break
                elif choice.content == "2":
                    await ctx.send(
                        "You fail to solve the riddle. The figure disappears, and you are lost."
                    )
                    break

            elif current_scene == "hidden_passage":
                if choice.content == "1":
                    await ctx.send(
                        "The passage leads to a magical garden. You feel rejuvenated."
                    )
                    break
                elif choice.content == "2":
                    await ctx.send("The passage is a dead end. You have to backtrack.")
                    current_scene = "dark_path"


def setup(bot):
    bot.add_cog(AdventureGame(bot))

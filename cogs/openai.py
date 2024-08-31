import os
import discord
from discord.ext import commands

from utils.openai import ask_gpt, img_generation
from utils.utils import handle_error, send_large_message


class Openai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_channel_id = os.environ.get("ALLOWED_CHANNEL_ID")

    @discord.slash_command(
        name="chatgpt",
        description="Ask ChatGPT a question.",
    )
    async def chat_gpt(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        try:
            answer = ask_gpt(prompt)
            await send_large_message(ctx, answer)
        except:
            await ctx.followup.send("❌ An error occurred. Please try again later.")

    @discord.slash_command(
        name="dalle",
        description="Send a prompt to Dall E 3 for a custom image generation of your own.",
        help="Send a prompt and an optional quality(standard or hd) and an optional size(1024x1024 | 1024x1792 | 1792x1024) for image generation. Will default to standard quality and a square image if parameters aren't included.",
    )
    async def dall_e(
        self, ctx, prompt, quality="standard", size="standard", style="vivid"
    ):
        allowed_qualities = {"standard", "hd"}
        allowed_sizes = {
            "standard": "1024x1024",
            "wide": "1792x1024",
            "tall": "1024x1792",
        }
        allowed_styles = {"natural", "vivid"}
        await ctx.defer(ephemeral=True)
        try:
            if (
                quality in allowed_qualities
                and size in allowed_sizes
                and style in allowed_styles
            ):
                try:
                    image_url = img_generation(
                        prompt, quality, allowed_sizes[size], style
                    )
                except Exception as e:
                    handle_error(e)
                finally:
                    embed = discord.Embed(
                        title="AI Image",
                        description=prompt,
                        color=ctx.author.top_role.color,
                    )
                    embed.set_image(url=image_url)
                    await ctx.followup.send("Generation Complete!")
                    await ctx.send(reference=ctx.message, embed=embed)
            else:
                await ctx.followup.send("Invalid quality or size.")
        except:
            await ctx.followup.send("❌ An error occurred. Please try again later.")


def setup(bot):
    bot.add_cog(Openai(bot))

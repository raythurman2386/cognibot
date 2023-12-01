import os
import discord
from discord.ext import commands
from db.database import is_user_in_table

from utils.openai import ask_gpt, deploy_gallery, img_generation, upload_image
from utils.utils import handle_error, send_large_message


class Openai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_channel_id = os.environ.get("ALLOWED_CHANNEL_ID")

    @discord.slash_command(
        name="chatgpt",
        description="Send a prompt to ChatGPT",
    )
    async def chat_gpt(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        if is_user_in_table(str(ctx.author.id), "authorized_users"):
            answer = ask_gpt(prompt)
            await send_large_message(ctx, answer)
        else:
            await ctx.followup.send("You are not authorized for GPT commands")

    @discord.slash_command(
        name="dalle",
        description="Send a prompt to Dall E 3",
    )
    async def dall_e(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        if is_user_in_table(str(ctx.author.id), "authorized_users"):
            image_url = img_generation(prompt)
            try:
                saved_image = await upload_image(image_url)
                await deploy_gallery()
            except Exception as e:
                handle_error(e)
            finally:
                embed = discord.Embed(
                    title="AI Image", description=prompt, color=ctx.author.top_role.color
                )
                embed.set_image(url=image_url)
                await ctx.followup.send("Generation Complete!")
                await ctx.send(reference=ctx.message, embed=embed)
        else:
            await ctx.followup.send("You are not authorized for GPT commands")


def setup(bot):
    bot.add_cog(Openai(bot))

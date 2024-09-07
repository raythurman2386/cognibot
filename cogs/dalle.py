import discord
from discord.ext import commands
from discord import option
from openai import OpenAI as OpenAIClient
import cloudinary
import cloudinary.uploader
import requests
from utils.logger import app_logger
from utils.env import env_vars
from utils.utils import handle_error


class DallEModal(discord.ui.Modal):
    def __init__(self, cog, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cog = cog
        self.style = "natural"
        self.quality = "standard"
        self.size = "standard"

        self.add_item(
            discord.ui.InputText(label="Prompt", style=discord.InputTextStyle.long)
        )
        self.add_item(
            discord.ui.InputText(
                label="Quality", placeholder="standard or hd", required=False
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Size", placeholder="standard, wide, or tall", required=False
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Style", placeholder="vivid or natural", required=False
            )
        )

    async def callback(self, interaction: discord.Interaction):
        prompt = self.children[0].value
        quality = self.children[1].value or self.quality
        size = self.children[2].value or self.size
        style = self.children[3].value or self.style

        await interaction.response.send_message(
            "Generating your image... This may take a moment.", ephemeral=True
        )

        try:
            image_url = await self.cog._img_generation(
                prompt, quality, size, style, interaction
            )

            embed = discord.Embed(
                title="AI Image",
                description=prompt,
                color=interaction.user.top_role.color,
            )
            embed.set_image(url=image_url)
            await interaction.followup.send("Generation Complete!", ephemeral=True)
            await interaction.channel.send(embed=embed)
            self.stop()
        except Exception as e:
            await interaction.followup.send(
                f"❌ An error occurred: {str(e)}", ephemeral=True
            )


class DALLE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAIClient()

        cloudinary.config(
            cloud_name=env_vars["cloud_name"],
            api_key=env_vars["cloudinary_api_key"],
            api_secret=env_vars["cloudinary_api_secret"],
        )

    @discord.slash_command(
        name="dalle",
        description="Send a prompt to Dall E 3 for a custom image generation of your own.",
    )
    async def dall_e(self, ctx):
        modal = DallEModal(self, title="DALL-E Image Generation")
        await ctx.send_modal(modal)

    @discord.slash_command(
        name="dalle_quick",
        description="Quickly generate an image with DALL-E using default settings.",
    )
    @option("prompt", str, description="The prompt for image generation", required=True)
    async def dall_e_quick(self, ctx, prompt: str):
        await ctx.respond(
            "Generating your image... This may take a moment.", ephemeral=True
        )
        try:
            image_url = await self._img_generation(
                prompt, "standard", "standard", "natural", ctx.interaction
            )
            embed = discord.Embed(
                title="AI Image",
                description=prompt,
                color=ctx.author.top_role.color,
            )
            embed.set_image(url=image_url)
            await ctx.followup.send("Generation Complete!", ephemeral=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.followup.send(f"❌ An error occurred: {str(e)}", ephemeral=True)

    async def _img_generation(self, prompt, quality, size, style, interaction=None):
        allowed_qualities = {"standard", "hd"}
        allowed_sizes = {
            "standard": "1024x1024",
            "wide": "1792x1024",
            "tall": "1024x1792",
        }
        allowed_styles = {"natural", "vivid"}

        if quality not in allowed_qualities:
            quality = "standard"
        if size not in allowed_sizes:
            size = "standard"
        if style not in allowed_styles:
            style = "vivid"

        try:
            if interaction:
                await interaction.edit_original_response(content="Generating image...")

            response = self.client.images.generate(
                model=env_vars["image_model"],
                prompt=prompt,
                size=allowed_sizes[size],
                quality=quality,
                style=style,
                n=1,
            )

            if interaction:
                await interaction.edit_original_response(
                    content="Image generated. Downloading..."
                )

            img_url = response.data[0].url
            app_logger.info("Image Successfully Generated")
            img_data = requests.get(img_url).content
            app_logger.info("Image Successfully Downloaded")

            if interaction:
                await interaction.edit_original_response(
                    content="Image downloaded. Uploading..."
                )

            upload_result = await self._upload_image(image_bytes=img_data)

            if interaction:
                await interaction.edit_original_response(
                    content="Image uploaded. Finalizing..."
                )

            return upload_result["secure_url"]
        except Exception as e:
            app_logger.error(f"❌ Image Generation Failed: {e}")
            return handle_error(e)

    async def _upload_image(self, image_bytes):
        folder_name = env_vars["cloudinary_folder"]
        try:
            response = cloudinary.uploader.upload(image_bytes, folder=folder_name)
            app_logger.info("Image uploaded successfully")
            await self._deploy_gallery()
            return response
        except Exception as e:
            app_logger.error(f"❌ Failed to upload image: {e}")
            return handle_error(e)

    async def _deploy_gallery(self):
        deploy_hook_url = env_vars["deploy_hook"]

        try:
            response = requests.post(deploy_hook_url)
            if response.status_code == 201:
                app_logger.info("Deploy triggered successfully")
            else:
                app_logger.warning(
                    f"❌ Failed to trigger deploy. Status code: {response.status_code}"
                )
        except Exception as e:
            app_logger.error(f"❌ Failed to trigger deploy: {e}")
            return handle_error(e)


def setup(bot):
    bot.add_cog(DALLE(bot))

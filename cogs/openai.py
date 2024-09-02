import discord
from discord.ext import commands
from db.database import ChatDatabase
from utils.utils import handle_error, send_large_message
from openai import OpenAI as OpenAIClient
import cloudinary
import cloudinary.uploader
import requests
from utils.logger import app_logger
from utils.env import env_vars


class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = ChatDatabase()
        self.client = OpenAIClient()

        cloudinary.config(
            cloud_name=env_vars["cloud_name"],
            api_key=env_vars["cloudinary_api_key"],
            api_secret=env_vars["cloudinary_api_secret"],
        )

    @discord.slash_command(
        name="chatgpt",
        description="Ask ChatGPT a question.",
    )
    async def chat_gpt(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        try:
            user_id = str(ctx.author.id)
            answer = self._ask_gpt(user_id, prompt)
            await send_large_message(ctx, answer)
        except Exception as e:
            await ctx.followup.send(f"❌ An error occurred: {str(e)}")

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
                image_url = self._img_generation(
                    prompt, quality, allowed_sizes[size], style
                )
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
        except Exception as e:
            await ctx.followup.send(f"❌ An error occurred: {str(e)}")

    def _ask_gpt(self, user_id, question):
        try:
            if len(question) == 0:
                raise ValueError("Please provide a question for ChatGPT!")

            self.db.add_message(user_id, "user", question)
            app_logger.info(f"User message added to database for user {user_id}")

            chat_log = self.db.get_chat_log(user_id)

            response = self.client.chat.completions.create(
                model=env_vars["gpt_model"],
                messages=chat_log,
                temperature=0.3,
                max_tokens=500,
            )
            answer = response.choices[0].message.content
            app_logger.info(f"ChatGPT generation successful for user {user_id}")

            self.db.add_message(user_id, "assistant", answer)
            app_logger.info(f"ChatGPT message added to database for user {user_id}")

            return answer
        except Exception as e:
            app_logger.error(
                f"❌ GPT generation encountered an error for user {user_id}: {e}"
            )
            return handle_error(e)

    def _img_generation(self, prompt, quality, size, style):
        try:
            response = self.client.images.generate(
                model=env_vars["image_model"],
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1,
            )

            img_url = response.data[0].url
            app_logger.info("Image Successfully Generated")
            # Download image from DALL-E URL
            img_data = requests.get(img_url).content
            app_logger.info("Image Successfully Downloaded")

            upload_result = self._upload_image(image_bytes=img_data)
            return upload_result["secure_url"]
        except Exception as e:
            app_logger.error(f"❌ Image Generation Failed: {e}")
            return handle_error(e)

    def _upload_image(self, image_bytes):
        folder_name = env_vars["cloudinary_folder"]
        try:
            response = cloudinary.uploader.upload(image_bytes, folder=folder_name)
            app_logger.info("Image uploaded successfully")
            self._deploy_gallery()
            return response
        except Exception as e:
            app_logger.error(f"❌ Failed to upload image: {e}")
            return handle_error(e)

    def _deploy_gallery(self):
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
    bot.add_cog(OpenAI(bot))

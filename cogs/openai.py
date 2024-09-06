import discord
from discord.ext import commands
from db.database import ChatDatabase
from utils.utils import handle_error, send_large_message
from openai import OpenAI as OpenAIClient
from utils.logger import app_logger
from utils.env import env_vars


class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = ChatDatabase()
        self.client = OpenAIClient()

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


def setup(bot):
    bot.add_cog(OpenAI(bot))

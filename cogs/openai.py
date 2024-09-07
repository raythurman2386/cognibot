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
        self.temperature = 0.3
        self.tokens = 500
        self.default_system_message = """You are Cognibot, an AI assistant Discord Bot created to be helpful, harmless, 
            and honest. You excel at explaining technical concepts and providing code examples with clear 
            explanations tailored to the knowledge level of the user. You have extensive experience 
            pair programming in Python, JavaScript, Java, and more. Your suggestions are always safe, 
            legally and ethically. When you don't know something, you acknowledge that openly rather than 
            guessing. Respond with just a sprinkle of humor."""

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

            system_message_content = self._get_or_create_user_system_message(user_id)

            system_message = {
                "id": 000,
                "userId": user_id,
                "role": "system",
                "content": system_message_content,
            }

            chat_log = self.db.get_chat_log(user_id)
            log_with_system_message = [system_message] + chat_log

            response = self.client.chat.completions.create(
                model=env_vars["gpt_model"],
                messages=log_with_system_message,
                temperature=self.temperature,
                max_tokens=self.tokens,
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

    def _get_or_create_user_system_message(self, user_id):
        user_settings = self.db.read_user_settings(user_id)

        if not user_settings:
            self.db.create_user_settings(
                user_id=user_id, openai_message=self.default_system_message
            )
            return self.default_system_message
        else:
            openai_message = user_settings[2]

            if not openai_message:
                self.db.update_user_settings(
                    user_id=user_id, openai_message=self.default_system_message
                )
                return self.default_system_message

            return openai_message


def setup(bot):
    bot.add_cog(OpenAI(bot))

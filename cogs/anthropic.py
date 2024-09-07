import discord
from discord.ext import commands
from db.database import ChatDatabase
from utils.utils import send_large_message, CustomError, handle_error
from anthropic import Anthropic as AnthropicClient
from utils.logger import app_logger
from utils.env import env_vars


class Anthropic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = ChatDatabase()
        self.anthropic = AnthropicClient(api_key=env_vars["anthropic_key"])
        self.temperature = 0.3
        self.tokens = 500
        self.default_system_message = """You are Cognibot, an AI assistant Discord Bot created to be helpful, harmless, 
            and honest. You excel at explaining technical concepts and providing code examples with clear 
            explanations tailored to the knowledge level of the user. You have extensive experience 
            pair programming in Python, JavaScript, Java, and more. Your suggestions are always safe, 
            legally and ethically. When you don't know something, you acknowledge that openly rather than 
            guessing. Respond with just a sprinkle of humor."""

    @discord.slash_command(
        name="claude",
        description="Send a prompt to Anthropic's Claude API",
    )
    async def claude(self, ctx, prompt):
        await ctx.defer(ephemeral=True)
        try:
            user_id = str(ctx.author.id)
            answer = self._ask_claude(user_id, prompt)
            await send_large_message(ctx, answer)
        except Exception as e:
            await ctx.followup.send(f"❌ An error occurred: {str(e)}")

    @discord.slash_command(
        name="clear_chat",
        description="Clear your chat history",
    )
    async def clear_chat(self, ctx):
        user_id = str(ctx.author.id)
        self.db.clear_user_chat_log(user_id)
        await ctx.respond("Your chat history has been cleared.", ephemeral=True)

    def _ask_claude(self, user_id, question):
        try:
            if len(question) == 0:
                raise CustomError("Please provide a question for Claude!")

            self.db.add_message(user_id, "user", question)
            app_logger.info(f"User message added to database for user {user_id}")

            system_message_content = self._get_or_create_user_system_message(user_id)

            chat_log = self.db.get_chat_log(user_id)

            response = self.anthropic.messages.create(
                model=env_vars["claude_model"],
                max_tokens=self.tokens,
                temperature=self.temperature,
                system=system_message_content,
                messages=chat_log,
            )

            answer = response.content[0].text
            app_logger.info(f"Claude generation successful for user {user_id}")
            self.db.add_message(user_id, "assistant", answer)
            app_logger.info(f"Assistant message added to database for user {user_id}")

            return answer
        except Exception as e:
            app_logger.error(
                f"❌ Claude generation encountered an error for user {user_id}: {e}"
            )
            return handle_error(e)

    def _get_or_create_user_system_message(self, user_id):
        user_settings = self.db.read_user_settings(user_id)

        if not user_settings:
            self.db.create_user_settings(
                user_id=user_id, anthropic_message=self.default_system_message
            )
            return self.default_system_message
        else:
            anthropic_message = user_settings[3]

            if not anthropic_message:
                self.db.update_user_settings(
                    user_id=user_id, anthropic_message=self.default_system_message
                )
                return self.default_system_message

            return anthropic_message


def setup(bot):
    bot.add_cog(Anthropic(bot))

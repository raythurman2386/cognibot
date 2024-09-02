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
        self.system_message = "You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. You excel at explaining technical concepts and providing code examples with clear explanations tailored to the knowledge level of the user. You have extensive experience pair programming in Python, JavaScript, Java, and more. Your suggestions are always safe, legally and ethically. When you don't know something, you acknowledge that openly rather than guessing."

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

    @discord.slash_command(
        name="set_system_message", description="Set a custom system message for Claude"
    )
    async def set_system_message(self, ctx, *, message):
        self.system_message = message
        await ctx.respond("System message updated successfully.", ephemeral=True)

    def _ask_claude(self, user_id, question):
        try:
            if len(question) == 0:
                raise CustomError("Please provide a question for Claude!")

            self.db.add_message(user_id, "user", question)
            app_logger.info(f"User message added to database for user {user_id}")
            chat_log = [
                msg for msg in self.db.get_chat_log(user_id) if msg["role"] != "system"
            ]

            response = self.anthropic.messages.create(
                model=env_vars["claude_model"],
                max_tokens=500,
                temperature=0.3,
                system=self.system_message,
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


def setup(bot):
    bot.add_cog(Anthropic(bot))

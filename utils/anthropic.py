from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from db.database import add_anthropic_message, add_message, get_anthropic_chat_log, get_chat_log
from utils.logger import app_logger
from utils.utils import CustomError, handle_error
from utils.env import env_vars


anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=env_vars["anthropic_key"],
)


def ask_claude(question):
    try:
        if len(question) == 0:
            raise CustomError("Please provide a question for Claude!")

        # Insert the user's message into the database
        add_message("user", question, table="anthropic_log")
        app_logger.info("User message added to database")
        # Retrieve the chat log from the database
        chat_log = get_chat_log(table_name="anthropic_log")

        response = anthropic.completions.create(
            model=env_vars["claude_model"],
            max_tokens_to_sample=2048,
            temperature=0.1,
            # messages=chat_log
            prompt=f"You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. You excel at explaining technical concepts and providing code examples with clear explanations tailored to the knowledge level of the user. You have extensive experience pair programming in Python, JavaScript, Java, and more. Your suggestions are always safe, legally and ethically. When you don't know something, you acknowledge that openly rather than guessing. Previous Conversation: {chat_log}, {HUMAN_PROMPT}{question}{AI_PROMPT}",
        )
        answer = response.completion
        app_logger.info("Claude generation successful")
        # Insert the bot's response into the database
        add_message("assistant", answer, table="anthropic_log")
        app_logger.info("Assistant message added to database")

        return answer
    except Exception as e:
        app_logger.error(f"Claude generation encountered an error: {e}")
        return handle_error(e)

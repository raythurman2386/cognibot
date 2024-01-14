from anthropic import Anthropic
from db.database import (
    add_message,
    get_chat_log,
)
from utils.logger import app_logger
from utils.utils import CustomError, handle_error
from utils.env import env_vars


anthropic = Anthropic(
    api_key=env_vars["anthropic_key"],
)


def ask_claude(question):
    try:
        if len(question) == 0:
            raise CustomError("Please provide a question for Claude!")

        add_message("user", question, table="anthropic_log")
        app_logger.info("User message added to database")

        chat_log = get_chat_log(table_name="anthropic_log")

        response = anthropic.beta.messages.create(
            model=env_vars["claude_model"],
            max_tokens=2048,
            temperature=0.1,
            messages=chat_log,
        )
        answer = response.content
        app_logger.info("Claude generation successful")

        add_message("assistant", answer, table="anthropic_log")
        app_logger.info("Assistant message added to database")

        return answer
    except Exception as e:
        app_logger.error(f"Claude generation encountered an error: {e}")
        return handle_error(e)

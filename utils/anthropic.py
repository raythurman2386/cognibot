from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from db.database import add_message, get_chat_log
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
        add_message("user", question)
        app_logger.info("User message added to database")
        # Retrieve the chat log from the database
        chat_log = get_chat_log()

        response = anthropic.completions.create(
            model=env_vars["claude_model"],
            max_tokens_to_sample=300,
            temperature=0.1,
            # messages=chat_log,
            prompt=f"You are Claude, a helpful pair programming bot who provides useful suggestions and explanations to programmers.{HUMAN_PROMPT}{question}{AI_PROMPT}",
        )
        answer = response.completion
        app_logger.info("Claude generation successful")
        # Insert the bot's response into the database
        add_message("assistant", answer)
        app_logger.info("Assistant message added to database")

        return answer
    except Exception as e:
        app_logger.error(f"Claude generation encountered an error: {e}")
        return handle_error(e)

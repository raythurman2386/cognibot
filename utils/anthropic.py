import os

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import load_dotenv
from db.database import add_message, get_chat_log

from utils.utils import CustomError, handle_error

load_dotenv()

env_vars = {
    "claude_model": os.environ.get("CLAUDE_MODEL") or "claude-2",
    "anthropic_key": os.environ.get("ANTHROPIC_API_KEY"),
}

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

        # Insert the bot's response into the database
        add_message("assistant", answer)

        return answer
    except Exception as e:
        return handle_error(e)

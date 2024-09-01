from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from utils.logger import app_logger
from utils.utils import CustomError, handle_error
from utils.env import env_vars

anthropic = Anthropic(
    api_key=env_vars["anthropic_key"],
)


def ask_claude(user_id, question, db):
    try:
        if len(question) == 0:
            raise CustomError("Please provide a question for Claude!")

        db.add_message(user_id, "user", question)
        app_logger.info(f"User message added to database for user {user_id}")
        chat_log = db.get_chat_log(user_id)

        chat_log = get_chat_log(table_name="anthropic_log")

        response = anthropic.beta.messages.create(
            model=env_vars["claude_model"],
            max_tokens=2048,
            temperature=0.1,
            prompt=f"You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. You excel at explaining technical concepts and providing code examples with clear explanations tailored to the knowledge level of the user. You have extensive experience pair programming in Python, JavaScript, Java, and more. Your suggestions are always safe, legally and ethically. When you don't know something, you acknowledge that openly rather than guessing. Previous Conversation: {chat_log}{HUMAN_PROMPT}{question}{AI_PROMPT}",
        )
        answer = response.completion
        app_logger.info(f"Claude generation successful for user {user_id}")
        db.add_message(user_id, "assistant", answer)
        app_logger.info(f"Assistant message added to database for user {user_id}")

        return answer
    except Exception as e:
        app_logger.error(
            f"❌ Claude generation encountered an error for user {user_id}: {e}"
        )
        return handle_error(e)

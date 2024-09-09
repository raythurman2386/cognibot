import os
import sqlite3
from contextlib import contextmanager

from utils.env import env_vars


class ChatDatabase:
    def __init__(self, db_name="chat_log.sqlite"):
        self.db_dir = "db"
        self.db_path = (
            db_name if os.path.dirname(db_name) else f"{self.db_dir}/{db_name}"
        )
        self._ensure_db_directory()
        self.TABLE_DEFINITIONS = {
            "chat_log": """
            CREATE TABLE IF NOT EXISTS chat_log (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                role TEXT,
                content TEXT
            )
        """,
            "user_system_settings": """
            CREATE TABLE IF NOT EXISTS user_system_settings (
                id INTEGER PRIMARY KEY,
                user_id TEXT UNIQUE,
                openai_system_message TEXT DEFAULT '',
                anthropic_system_message TEXT DEFAULT '',
                temperature REAL DEFAULT 0.3,
                tokens INTEGER DEFAULT 500
            )
        """,
        }

    def _ensure_db_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    @contextmanager
    def _db_session(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            yield c
        finally:
            conn.commit()
            conn.close()

    def init_db(self):
        with self._db_session() as c:
            for table_name, create_statement in self.TABLE_DEFINITIONS.items():
                c.execute(create_statement)

    # CRUD Operations for chat_log
    def add_message(self, user_id, role, content):
        with self._db_session() as c:
            c.execute(
                "INSERT INTO chat_log (user_id, role, content) VALUES (?, ?, ?)",
                (user_id, role, content),
            )

    def get_chat_log(self, user_id):
        with self._db_session() as c:
            c.execute(
                "SELECT role, content FROM chat_log WHERE user_id = ? ORDER BY id",
                (user_id,),
            )
            chat_log = [
                {"role": role, "content": content} for role, content in c.fetchall()
            ]
        return chat_log

    def clear_user_chat_log(self, user_id):
        with self._db_session() as c:
            c.execute(
                "DELETE FROM chat_log WHERE user_id = ?",
                (user_id,),
            )

    # CRUD Operations for user_system_settings
    def create_user_settings(
        self,
        user_id,
        openai_message=env_vars["default_system_message"],
        anthropic_message=env_vars["default_system_message"],
        temperature=0.3,
        tokens=500,
    ):
        with self._db_session() as c:
            c.execute(
                """
                INSERT INTO user_system_settings (user_id, openai_system_message, anthropic_system_message, temperature, tokens)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, openai_message, anthropic_message, temperature, tokens),
            )
        return self.read_user_settings(user_id)

    def read_user_settings(self, user_id):
        with self._db_session() as c:
            c.execute(
                "SELECT * FROM user_system_settings WHERE user_id = ?", (user_id,)
            )
            settings = c.fetchone()
        return settings

    def update_user_settings(
        self,
        user_id,
        openai_message=None,
        anthropic_message=None,
        temperature=None,
        tokens=None,
    ):
        with self._db_session() as c:
            # Get current settings
            c.execute(
                "SELECT openai_system_message, anthropic_system_message, temperature, tokens FROM user_system_settings WHERE user_id = ?",
                (user_id,),
            )
            current_settings = c.fetchone()

            # Update fields only if new values are provided, otherwise keep current
            openai_message = openai_message or current_settings[0]
            anthropic_message = anthropic_message or current_settings[1]
            temperature = (
                temperature if temperature is not None else current_settings[2]
            )
            tokens = tokens if tokens is not None else current_settings[3]

            c.execute(
                """
                UPDATE user_system_settings
                SET openai_system_message = ?, anthropic_system_message = ?, temperature = ?, tokens = ?
                WHERE user_id = ?
                """,
                (openai_message, anthropic_message, temperature, tokens, user_id),
            )

    def delete_user_settings(self, user_id):
        with self._db_session() as c:
            c.execute(
                "DELETE FROM user_system_settings WHERE user_id = ?",
                (user_id,),
            )

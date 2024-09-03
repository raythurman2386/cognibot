import os
import sqlite3
from contextlib import contextmanager


class ChatDatabase:
    def __init__(self, db_name="chat_log.sqlite"):
        self.db_dir = "db"
        self.db_path = (
            db_name if os.path.dirname(db_name) else f"{self.db_dir}/{db_name}"
        )
        self._ensure_db_directory()

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
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_log (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    role TEXT,
                    content TEXT
                )
            """
            )

    def _ensure_system_message(self, user_id):
        with self._db_session() as c:
            c.execute(
                "SELECT COUNT(*) FROM chat_log WHERE user_id = ? AND role = 'system'",
                (user_id,),
            )
            system_entry_exists = c.fetchone()[0]

            if not system_entry_exists:
                c.execute(
                    "INSERT INTO chat_log (user_id, role, content) VALUES (?, ?, ?)",
                    (
                        user_id,
                        "system",
                        "You are a helpful, Discord bot. Respond with markdown as accurately as possible to the commands, with just a sprinkle of humor.",
                    ),
                )

    def add_message(self, user_id, role, content):
        self._ensure_system_message(user_id)
        with self._db_session() as c:
            c.execute(
                "INSERT INTO chat_log (user_id, role, content) VALUES (?, ?, ?)",
                (user_id, role, content),
            )

    def get_chat_log(self, user_id):
        self._ensure_system_message(user_id)
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
                "DELETE FROM chat_log WHERE user_id = ? AND role != 'system'",
                (user_id,),
            )
        self._ensure_system_message(user_id)

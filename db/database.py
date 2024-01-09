import psycopg2
from contextlib import contextmanager
from utils.logger import app_logger


@contextmanager  
def db_session():
    conn = psycopg2.connect(dbname="cognibot", user="postgres", password="admin")
    cursor = conn.cursor()
    app_logger.info(f"PGDatabase Connected Successfully")
    try: 
        yield cursor
    except:
        conn.rollback() 
        raise
    finally:
        try:
            cursor.close() 
            conn.close()
        except Exception:
            pass
        


def init_db():
    with db_session() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_log (
                id SERIAL PRIMARY KEY,
                role TEXT,
                content TEXT
            )
        """
        )
        # Check if the system entry already exists
        # Execute query 
        c.execute("SELECT COUNT(*) FROM chat_log WHERE role = 'system'")

        # Fetch one result 
        system_entry_exists = c.fetchone()[0]

        # If it doesn't exist, insert the default system entry
        if not system_entry_exists:
            c.execute(
                "INSERT INTO chat_log (id, role, content) VALUES (%s, %s, %s)",
                (
                    1,
                    "system",
                    "You are a helpful, Discord bot. Respond with markdown as accurately as possible to the commands, with just a sprinkle of humor.",
                ),
            )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS authorized_users (
                id SERIAL PRIMARY KEY,
                user_id TEXT
            )
        """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS moderators (
                id SERIAL PRIMARY KEY,
                user_id TEXT
            )
        """
        )
        c.execute("COMMIT")


def get_user_from_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name} WHERE user_id = {user_id}")
        user = c.fetchone()
    return user


def add_user_to_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"INSERT INTO {table_name} (user_id) VALUES ({user_id})")


def update_user_in_table(user_id, table_name, column_name, new_value):
    with db_session() as c:
        c.execute(
            f"UPDATE {table_name} SET {column_name} = {new_value} WHERE user_id = {user_id}"
        )


def remove_user_from_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"DELETE FROM {table_name} WHERE user_id={user_id}")


def is_user_in_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name} WHERE user_id='{str(user_id)}'") 
        result = c.fetchone()
    return result is not None


def get_user_from_table(user_id, table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name} WHERE user_id = '{str(user_id)}'")
        user = c.fetchone()
    return user


def get_all_users_from_table(table_name):
    with db_session() as c:
        c.execute(f"SELECT * FROM {table_name}")
        users = c.fetchall()
    return users


def count_users_in_table(table_name):
    with db_session() as c:
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = c.fetchone()[0]
    return count


def clear_table(table_name):
    with db_session() as c:
        c.execute(f"DELETE FROM {table_name}")


def add_message(role, content):
    with db_session() as c:
        c.execute("INSERT INTO chat_log (role, content) VALUES (%s, %s)", (role, content))


def get_chat_log():
    with db_session() as c:
        c.execute("SELECT role, content FROM chat_log")
        chat_log = [
            {"role": role, "content": content} for role, content in c.fetchall()
        ]
    return chat_log

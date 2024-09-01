import sys
import pytest
import sqlite3
import os
from contextlib import contextmanager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db.database import ChatDatabase


@pytest.fixture(scope="function")
def test_db(tmp_path):
    test_db_path = tmp_path / "test_chat_log.sqlite"
    db = ChatDatabase(str(test_db_path))
    db.init_db()
    yield db
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


def test_init_db(test_db):
    with test_db._db_session() as c:
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
    assert ("chat_log",) in tables


def test_add_and_get_chat_log(test_db):
    user_id = "12345"
    test_db.add_message(user_id, "user", "Hello, bot!")
    test_db.add_message(user_id, "assistant", "Hello! How can I help you?")

    chat_log = test_db.get_chat_log(user_id)
    assert len(chat_log) == 3  # Including the system message
    assert chat_log[1]["role"] == "user"
    assert chat_log[1]["content"] == "Hello, bot!"
    assert chat_log[2]["role"] == "assistant"
    assert chat_log[2]["content"] == "Hello! How can I help you?"


def test_clear_user_chat_log(test_db):
    user_id = "67890"
    test_db.add_message(user_id, "user", "Test message")
    test_db.clear_user_chat_log(user_id)

    chat_log = test_db.get_chat_log(user_id)
    assert len(chat_log) == 1  # Only the system message should remain
    assert chat_log[0]["role"] == "system"


def test_multiple_users(test_db):
    user1_id = "user1"
    user2_id = "user2"

    test_db.add_message(user1_id, "user", "Hello from user1")
    test_db.add_message(user2_id, "user", "Hello from user2")

    chat_log1 = test_db.get_chat_log(user1_id)
    chat_log2 = test_db.get_chat_log(user2_id)

    assert len(chat_log1) == 2  # System message + user message
    assert len(chat_log2) == 2
    assert chat_log1[1]["content"] == "Hello from user1"
    assert chat_log2[1]["content"] == "Hello from user2"


def test_ensure_system_message(test_db):
    user_id = "test_user"

    # First message should trigger system message creation
    test_db.add_message(user_id, "user", "First message")
    chat_log = test_db.get_chat_log(user_id)

    assert len(chat_log) == 2
    assert chat_log[0]["role"] == "system"

    # Clear chat log and check if system message is recreated
    test_db.clear_user_chat_log(user_id)
    chat_log = test_db.get_chat_log(user_id)

    assert len(chat_log) == 1
    assert chat_log[0]["role"] == "system"

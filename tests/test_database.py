import sys
import pytest
import sqlite3
import os
from contextlib import contextmanager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.database import (
    db_session,
    init_db,
    add_user_to_table,
    remove_user_from_table,
    is_user_in_table,
    get_user_from_table,
    get_all_users_from_table,
    count_users_in_table,
    clear_table,
    add_message,
    get_chat_log,
)

@pytest.fixture(scope="function")
def test_db():
    test_db_path = "test_chat_log.sqlite"
    conn = sqlite3.connect(test_db_path)
    conn.close()
    
    @contextmanager
    def test_db_session():
        conn = sqlite3.connect(test_db_path)
        c = conn.cursor()
        try:
            yield c
        finally:
            conn.commit()
            conn.close()
    
    from db import database
    database.db_session = test_db_session

    init_db()
    
    yield
    
    # Clean up the test database after tests
    os.remove(test_db_path)

def test_init_db(test_db):
    with db_session() as c:
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
    assert ('chat_log',) in tables
    assert ('authorized_users',) in tables
    assert ('moderators',) in tables

def test_add_and_remove_user(test_db):
    user_id = "12345"
    table_name = "authorized_users"
    
    add_user_to_table(user_id, table_name)
    assert is_user_in_table(user_id, table_name)
    
    remove_user_from_table(user_id, table_name)
    assert not is_user_in_table(user_id, table_name)

def test_get_user_from_table(test_db):
    user_id = "67890"
    table_name = "moderators"
    
    add_user_to_table(user_id, table_name)
    user = get_user_from_table(user_id, table_name)
    assert user is not None
    assert user[1] == user_id

def test_get_all_users_from_table(test_db):
    table_name = "authorized_users"
    add_user_to_table("user1", table_name)
    add_user_to_table("user2", table_name)
    
    users = get_all_users_from_table(table_name)
    assert len(users) == 2

def test_count_users_in_table(test_db):
    table_name = "moderators"
    add_user_to_table("mod1", table_name)
    add_user_to_table("mod2", table_name)
    add_user_to_table("mod3", table_name)
    
    count = count_users_in_table(table_name)
    assert count == 3

def test_clear_table(test_db):
    table_name = "authorized_users"
    add_user_to_table("user1", table_name)
    add_user_to_table("user2", table_name)
    
    clear_table(table_name)
    count = count_users_in_table(table_name)
    assert count == 0

def test_add_and_get_chat_log(test_db):
    add_message("user", "Hello, bot!")
    add_message("assistant", "Hello! How can I help you?")
    
    chat_log = get_chat_log()
    assert len(chat_log) == 3 
    assert chat_log[1]["role"] == "user"
    assert chat_log[1]["content"] == "Hello, bot!"
    assert chat_log[2]["role"] == "assistant"
    assert chat_log[2]["content"] == "Hello! How can I help you?"

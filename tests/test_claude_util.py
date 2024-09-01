import pytest
from unittest.mock import Mock, patch
from anthropic import Anthropic
from anthropic.types import ContentBlock, Message
from utils.utils import CustomError, handle_error

from utils.anthropic import ask_claude

@pytest.fixture
def mock_db():
    db = Mock()
    db.add_message = Mock()
    db.get_chat_log = Mock(return_value=[
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ])
    return db

@pytest.fixture
def mock_anthropic():
    with patch('utils.anthropic') as mock:
        mock.messages.create.return_value = Mock(
            content=[Mock(text="This is a test response", type="text")]
        )
        yield mock


def test_ask_claude_db_error(mock_db, mock_anthropic):
    mock_db.add_message.side_effect = Exception("Database error")
    
    result = ask_claude("user123", "What is Python?", mock_db)
    
    assert isinstance(result, str)
    assert "An error occurred" in result

def test_ask_claude_anthropic_error(mock_db, mock_anthropic):
    mock_anthropic.messages.create.side_effect = Exception("API error")
    
    result = ask_claude("user123", "What is Python?", mock_db)
    
    assert isinstance(result, str)
    assert "An error occurred" in result
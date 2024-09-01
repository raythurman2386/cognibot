import os
import pytest
from unittest.mock import patch, MagicMock
from utils.openai import img_generation, ask_gpt, upload_image, deploy_gallery
from utils.utils import CustomError

@pytest.fixture
def mock_openai_client():
    with patch('utils.openai.client') as mock_client:
        yield mock_client

@pytest.fixture
def mock_requests():
    with patch('utils.openai.requests') as mock_requests:
        yield mock_requests

@pytest.fixture
def mock_cloudinary():
    with patch('utils.openai.cloudinary.uploader') as mock_cloudinary:
        yield mock_cloudinary

@pytest.fixture
def mock_db():
    return MagicMock()

def test_img_generation_success(mock_openai_client, mock_requests, mock_cloudinary):
    mock_openai_client.images.generate.return_value.data = [MagicMock(url='http://fake-image-url')]
    mock_requests.get.return_value.content = b'fake image content'
    mock_cloudinary.upload.return_value = {'secure_url': 'http://uploaded-image-url'}

    result = img_generation('test prompt', 'standard', '1024x1024', 'vivid')

    assert result == 'http://uploaded-image-url'
    mock_openai_client.images.generate.assert_called_once()
    mock_requests.get.assert_called_once_with('http://fake-image-url')
    mock_cloudinary.upload.assert_called_once()

def test_img_generation_failure(mock_openai_client):
    mock_openai_client.images.generate.side_effect = Exception('API Error')

    result = img_generation('test prompt', 'standard', '1024x1024', 'vivid')

    assert "An error occurred" in result

def test_ask_gpt_success(mock_openai_client, mock_db):
    mock_db.get_chat_log.return_value = [{'role': 'user', 'content': 'Hello'}]
    mock_openai_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content='GPT response'))
    ]

    result = ask_gpt('user123', 'Hello', mock_db)

    assert result == 'GPT response'
    mock_db.add_message.assert_called()
    mock_openai_client.chat.completions.create.assert_called_once()

def test_ask_gpt_failure(mock_openai_client, mock_db):
    mock_openai_client.chat.completions.create.side_effect = Exception('API Error')

    result = ask_gpt('user123', 'Hello', mock_db)

    assert "An error occurred" in result

def test_upload_image_success(mock_cloudinary):
    mock_cloudinary.upload.return_value = {'secure_url': 'http://uploaded-image-url'}

    result = upload_image(b'fake image content')

    assert result == {'secure_url': 'http://uploaded-image-url'}
    mock_cloudinary.upload.assert_called_once()

def test_upload_image_failure(mock_cloudinary):
    mock_cloudinary.upload.side_effect = Exception('Upload Error')

    result = upload_image(b'fake image content')

    assert "An error occurred" in result

def test_deploy_gallery_success(mock_requests):
    mock_requests.post.return_value.status_code = 201

    deploy_gallery()

    mock_requests.post.assert_called_once()

def test_deploy_gallery_failure(mock_requests):
    mock_requests.post.side_effect = Exception('Deploy Error')

    result = deploy_gallery()

    assert "An error occurred" in result


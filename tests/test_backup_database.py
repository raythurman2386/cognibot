import os
import pytest
import shutil
import time
from unittest.mock import MagicMock, patch
from db.backup import backup_database

@pytest.fixture
def setup_test_environment(tmp_path):
    db_dir = tmp_path / "db"
    db_dir.mkdir()
    backup_dir = tmp_path / "Backups"
    db_path = db_dir / "chat_log.sqlite"
    db_path.write_text("This is a dummy database")
    yield db_path, backup_dir
    shutil.rmtree(tmp_path)

@pytest.fixture
def mock_logger():
    with patch('utils.logger.app_logger') as mock_logger:
        yield mock_logger

def test_backup_creates_backup_folder(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    assert backup_dir.exists()

def test_backup_creates_backup_file(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    assert len(list(backup_dir.glob("*.db"))) == 1

def test_backup_file_name_format(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    backup_file = list(backup_dir.glob("*.db"))[0]
    assert backup_file.name.startswith("chat_log_backup_")
    assert backup_file.name.endswith(".db")

def test_backup_file_content(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    backup_file = list(backup_dir.glob("*.db"))[0]
    assert backup_file.read_text() == "This is a dummy database"

def test_backup_respects_max_size(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    with db_path.open("wb") as f:
        f.write(b"0" * (2 * 1024 * 1024))
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir), max_size_mb=1)
    assert len(list(backup_dir.glob("*.db"))) == 1
    mock_logger.warning.assert_called_once()

def test_multiple_backups(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    time.sleep(1)
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    assert len(list(backup_dir.glob("*.db"))) == 2

def test_backup_logs_info(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    assert mock_logger.info.call_count == 2

def test_backup_handles_errors(setup_test_environment, mock_logger):
    db_path, backup_dir = setup_test_environment
    with patch('shutil.copy2', side_effect=Exception("Test error")):
        backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    mock_logger.error.assert_called_once()

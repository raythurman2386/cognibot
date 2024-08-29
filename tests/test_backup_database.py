import os
import pytest
import shutil
import time
from db.backup import backup_database

@pytest.fixture
def setup_test_environment(tmp_path):
    # Create a temporary directory for our test database and backups
    db_dir = tmp_path / "db"
    db_dir.mkdir()
    backup_dir = tmp_path / "Backups"
    
    # Create a dummy database file
    db_path = db_dir / "chat_log.sqlite"
    db_path.write_text("This is a dummy database")
    
    yield db_path, backup_dir
    
    # Cleanup (pytest should handle this automatically, but just in case)
    shutil.rmtree(tmp_path)

def test_backup_creates_backup_folder(setup_test_environment):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    assert backup_dir.exists()

def test_backup_creates_backup_file(setup_test_environment):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    assert len(list(backup_dir.glob("*.db"))) == 1

def test_backup_file_name_format(setup_test_environment):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    backup_file = list(backup_dir.glob("*.db"))[0]
    assert backup_file.name.startswith("chat_log_backup_")
    assert backup_file.name.endswith(".db")

def test_backup_file_content(setup_test_environment):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    backup_file = list(backup_dir.glob("*.db"))[0]
    assert backup_file.read_text() == "This is a dummy database"

def test_backup_respects_max_size(setup_test_environment):
    db_path, backup_dir = setup_test_environment
    # Create a 2MB file
    with db_path.open("wb") as f:
        f.write(b"0" * (2 * 1024 * 1024))
    
    # This should print a warning but still create the backup
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir), max_size_mb=1)
    assert len(list(backup_dir.glob("*.db"))) == 1

def test_multiple_backups(setup_test_environment):
    db_path, backup_dir = setup_test_environment
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    time.sleep(1)  # Ensure a different timestamp
    backup_database(db_path=str(db_path), backup_folder=str(backup_dir))
    assert len(list(backup_dir.glob("*.db"))) == 2


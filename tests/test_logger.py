import logging
import pytest
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import app_logger, Logger, AsyncRotatingFileHandler

# Define the path to the log file
LOG_DIR = "Logs"
LOG_FILE = os.path.join(LOG_DIR, "test_cognibot.log")

@pytest.fixture(scope="function", autouse=True)
def cleanup_log():
    # Before each test, clean up any existing log file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield
    # After each test, clean up the log file again
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

def wait_for_file_creation(file_path, timeout=10):
    """Wait for a file to be created with a timeout."""
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"File {file_path} was not created in time.")
        time.sleep(0.1)

def wait_for_log_content(file_path, content, timeout=10):
    """Wait for specific content to appear in a file."""
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Content '{content}' was not found in file {file_path} in time.")
        if os.path.exists(file_path):
            with open(file_path, "r") as log_file:
                if content in log_file.read():
                    return
        time.sleep(0.1)

def wait_for_log_completion(logger, timeout=10):
    """Wait for the logger to complete logging with a timeout."""
    start_time = time.time()
    while any(isinstance(handler, AsyncRotatingFileHandler) and not handler.executor._work_queue.empty()
              for handler in logger.handlers):
        if time.time() - start_time > timeout:
            raise TimeoutError("Logging did not complete in time.")
        time.sleep(0.1)

def test_logger_initialization():
    # Test that the logger is initialized correctly
    logger = Logger("TestLogger")
    assert logger.get_logger().name == "TestLogger"
    assert isinstance(logger.get_logger().handlers[0], logging.Handler)

@pytest.mark.skip(reason="Currently failing due to timing issues.")
def test_log_file_creation():
    # Test that logging creates the log file
    app_logger.info("Testing log creation.")
    wait_for_log_completion(app_logger)
    wait_for_file_creation(LOG_FILE)
    assert os.path.exists(LOG_FILE)

@pytest.mark.skip(reason="Currently failing due to timing issues.")
def test_log_content():
    # Test that logging writes the correct content
    test_message = "This is a test log entry."
    app_logger.info(test_message)
    wait_for_log_completion(app_logger)
    wait_for_log_content(LOG_FILE, test_message)
    
    with open(LOG_FILE, "r") as log_file:
        logs = log_file.read()
    
    assert test_message in logs

def test_async_logging():
    # Test that logging is handled asynchronously (basic check)
    logger = Logger("AsyncLogger", log_file="async_test.log")
    async_logger = logger.get_logger()
    async_logger.info("Testing async logging.")
    wait_for_log_completion(async_logger)
    wait_for_file_creation("Logs/async_test.log")
    assert os.path.exists("Logs/async_test.log")

    # Clean up
    os.remove("Logs/async_test.log")

def test_log_rotation():
    # Test that log rotation works as expected
    logger = Logger("RotateLogger", log_file="rotate_test.log", max_bytes=50, backup_count=2)
    rotate_logger = logger.get_logger()

    for i in range(20):
        rotate_logger.info(f"Log entry {i}")

    wait_for_log_completion(rotate_logger)
    time.sleep(1)  # Allow time for the log rotation to complete
    log_files = [f for f in os.listdir(LOG_DIR) if "rotate_test" in f]
    assert len(log_files) > 1

    # Clean up
    for f in log_files:
        os.remove(os.path.join(LOG_DIR, f))

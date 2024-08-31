#!/bin/bash

EXPECTED_DIR="cognibot"
CURRENT_DIR=${PWD##*/}

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Not in the $EXPECTED_DIR directory. Changing directory..."
    cd ./cognibot
fi

source venv/bin/activate

PYTHON_PATH="python"

$PYTHON_PATH << END
from db.backup import backup_database
from utils.logger import app_logger

try:
    backup_database()
    app_logger.info("Backup completed successfully.")
except Exception as e:
    app_logger.error(f"Backup failed: {str(e)}")
END

deactivate

echo "Backup process completed."

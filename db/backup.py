import os
import shutil
import time


def backup_database(
        db_path="db/chat_log.sqlite",
        backup_folder="Backups",
        max_size_mb=1024
):
    from utils.logger import app_logger

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    db_size = os.path.getsize(db_path) / (1024 * 1024)
    if db_size > max_size_mb:
        app_logger.warning(f"Database size ({db_size:.2f}MB) is over the limit of {max_size_mb}MB.")

    app_logger.info(f"Database size is currently {db_size:.2f}MB.")

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(backup_folder, f"chat_log_backup_{timestamp}.db")

    try:
        shutil.copy2(db_path, backup_path)
        app_logger.info(f"Database backed up to {backup_path}")
    except Exception as e:
        app_logger.error(f"Failed to backup database: {str(e)}")

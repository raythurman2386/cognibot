import os
import shutil
import time

def backup_database(db_path="db/chat_log.db", backup_folder="Backups", max_size_mb=1024):
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    db_size = os.path.getsize(db_path) / (1024 * 1024)  # Size in MB
    if db_size > max_size_mb:
        print(f"Database size ({db_size}MB) is over the limit of {max_size_mb}MB.")
        # app_logger.info(f"Database size ({db_size}MB) is over the limit of {max_size_mb}MB.")
        # Here you can call a function to clean up the database or raise an error

    print(f"Database size is currently {db_size}MB.")

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(backup_folder, f"chat_log_backup_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    print(f"Database backed up to {backup_path}")

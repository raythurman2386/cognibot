import os
import atexit
import logging
import signal
import sys
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor


class AsyncRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=2)

    def emit(self, record):
        self.executor.submit(self._emit, record)

    def _emit(self, record):
        try:
            super().emit(record)
        except (OSError, IOError) as e:
            self.handleError(record)

    def close(self):
        self.executor.shutdown(wait=True)
        super().close()


class Logger:
    def __init__(self, name: str, log_dir: str = "Logs", log_file: str = "cognibot.log", max_bytes: int = 1024 * 1024, backup_count: int = 3):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Set up the rotating file handler
        log_path = os.path.join(log_dir, log_file)
        handler = AsyncRotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        atexit.register(self.shutdown_logging)
        
    def setup_signal_handlers(self):
        signal.signal(signal.SIGTERM, self.handle_exit_signal)
        signal.signal(signal.SIGINT, self.handle_exit_signal)

    def shutdown_logging(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def handle_exit_signal(self, signum, frame):
        self.shutdown_logging()
        sys.exit(0)

    def get_logger(self):
        return self.logger


logger = Logger("CogniBotLogger")
app_logger = logger.get_logger()
logger.setup_signal_handlers()

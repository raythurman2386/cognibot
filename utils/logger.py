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

app_logger = logging.getLogger("CogniBotLogger")
app_logger.setLevel(logging.INFO)

try:
    handler = AsyncRotatingFileHandler(
        "cognibot.log", maxBytes=1024 * 1024, backupCount=3
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    app_logger.addHandler(handler)
except Exception as e:
    print(f"Failed to set up logger: {e}")

def shutdown_logging():
    handlers = app_logger.handlers[:]
    for handler in handlers:
        handler.close()
        app_logger.removeHandler(handler)

atexit.register(shutdown_logging)

def handle_exit_signal(signum, frame):
    shutdown_logging()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit_signal)
signal.signal(signal.SIGINT, handle_exit_signal)

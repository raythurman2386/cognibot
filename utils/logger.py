import logging
from logging.handlers import RotatingFileHandler

# Set up a specific logger with our desired output level
app_logger = logging.getLogger("CogniBotLogger")
app_logger.setLevel(logging.INFO)

# Add the log message handler to the logger
handler = RotatingFileHandler(
    "cognibot.log", maxBytes=1024 * 1024, backupCount=3  # 1 MB
)

# Create a formatter and set it for the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Add the handler to the logger
app_logger.addHandler(handler)

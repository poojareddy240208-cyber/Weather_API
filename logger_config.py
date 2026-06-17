from logging.handlers import RotatingFileHandler
import logging

file_handler = RotatingFileHandler(
    "app.log",
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=3
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        file_handler
    ]
)

logger = logging.getLogger("weather_api")
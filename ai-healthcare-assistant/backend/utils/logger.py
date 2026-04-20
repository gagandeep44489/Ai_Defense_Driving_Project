import logging
import sys
from pythonjsonlogger import jsonlogger

from utils.config import settings


def setup_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level.upper())

    if root_logger.handlers:
        root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

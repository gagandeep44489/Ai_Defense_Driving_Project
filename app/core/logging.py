import logging
import structlog


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    structlog.configure(processors=[structlog.processors.JSONRenderer()])

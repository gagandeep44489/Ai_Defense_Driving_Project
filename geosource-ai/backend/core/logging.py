"""Logging configuration."""
from __future__ import annotations

import logging


def configure_logging(level: str) -> None:
    """Configure process-wide logging with a structured format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

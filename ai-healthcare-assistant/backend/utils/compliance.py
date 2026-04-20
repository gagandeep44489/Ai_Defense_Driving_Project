import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


def audit_log(action: str, payload: dict[str, Any]) -> None:
    logger.info(
        "audit_event",
        extra={
            "action": action,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        },
    )

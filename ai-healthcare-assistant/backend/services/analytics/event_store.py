from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from typing import Any


@dataclass
class EventRecord:
    event_type: str
    timestamp: datetime
    payload: dict[str, Any]
    response_time_ms: float
    success: bool


class AnalyticsEventStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._events: list[EventRecord] = []

    def log_event(
        self,
        event_type: str,
        payload: dict[str, Any],
        response_time_ms: float,
        success: bool,
    ) -> None:
        record = EventRecord(
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            payload=payload,
            response_time_ms=response_time_ms,
            success=success,
        )
        with self._lock:
            self._events.append(record)

    def get_events_since(self, since: datetime) -> list[EventRecord]:
        with self._lock:
            return [event for event in self._events if event.timestamp >= since]


analytics_store = AnalyticsEventStore()

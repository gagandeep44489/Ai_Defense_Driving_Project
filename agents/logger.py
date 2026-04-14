"""Thought logging utilities for Saarthi AI."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ThoughtLogger:
    logs: List[str] = field(default_factory=list)

    def extend(self, thought_log: List[str]) -> None:
        self.logs.extend(thought_log)

    def to_text(self) -> str:
        return "\n".join(f"- {step}" for step in self.logs)

    def build_record(self, scenario: Dict[str, Any], payload: Dict[str, Any], latency_seconds: float, used_fallback: bool) -> Dict[str, Any]:
        return {
            "scenario": {"id": scenario.get("id"), "name": scenario.get("name")},
            "objects": payload.get("objects", []),
            "intent": payload.get("intent", {}),
            "risk": payload.get("risk", "Medium"),
            "decision": payload.get("decision", "Slow Down"),
            "thought_log": payload.get("thought_log", []),
            "latency_seconds": round(latency_seconds, 4),
            "used_fallback": used_fallback,
        }

    def save_json(self, output_path: str, record: Dict[str, Any]) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")

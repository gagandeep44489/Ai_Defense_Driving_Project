"""Perception agent for extracting objects from scenario data."""

from __future__ import annotations

from typing import Dict, List


class PerceptionAgent:
    """Minimal perception stage before LLM reasoning."""

    def detect(self, scenario: Dict) -> List[Dict]:
        return scenario.get("objects", [])

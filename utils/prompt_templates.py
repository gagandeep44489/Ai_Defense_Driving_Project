"""Prompt templates for Saarthi AI LLM reasoning."""

from __future__ import annotations

import json
from typing import Dict


SYSTEM_PROMPT = (
    "You are an autonomous driving safety AI for Indian roads. "
    "Reason carefully, keep the output deterministic, and return strict JSON only."
)


def build_reasoning_prompt(scenario: Dict) -> str:
    """Build a structured prompt that asks for strict JSON output."""

    input_payload = {
        "objects": [obj["type"] for obj in scenario.get("objects", [])],
        "distance": {obj["type"]: f"{obj.get('distance_m', '?')}m" for obj in scenario.get("objects", [])},
        "speed": {obj["type"]: f"{obj.get('speed_kmph', '?')} km/h" for obj in scenario.get("objects", [])},
        "ego_speed": f"{scenario.get('ego_speed_kmph', '?')} km/h",
        "context": "Indian unstructured road",
    }

    return f"""
SYSTEM:
{SYSTEM_PROMPT}

TASK:
Analyze the situation and provide:
1. Detected objects
2. Intent of each object
3. Risk level (Low/Medium/High)
4. Final decision
5. Thought process (step-by-step reasoning)

INPUT:
{json.dumps(input_payload, indent=2)}

OUTPUT FORMAT (STRICT JSON):
{{
  "objects": [],
  "intent": {{}},
  "risk": "",
  "decision": "",
  "thought_log": []
}}

Rules:
- Return valid JSON only, no markdown.
- Keep thought_log concise but explicit.
- If braking is dangerous due to rear traffic, prefer safer avoid/slow maneuver.
""".strip()

"""Decision post-processor for LLM output safety normalization."""

from __future__ import annotations

from typing import Dict


class DecisionAgent:
    """Validates and normalizes final decisions from the LLM."""

    VALID = {"Brake", "Slow Down", "Turn", "Continue", "Avoid", "Avoid pothole without hard braking", "Continue with caution"}

    def finalize(self, llm_payload: Dict) -> str:
        decision = llm_payload.get("decision", "Slow Down")
        if decision in self.VALID:
            return decision

        normalized = decision.lower()
        if "turn" in normalized:
            return "Turn"
        if "brake" in normalized:
            return "Brake"
        if "avoid" in normalized:
            return "Avoid"
        if "slow" in normalized:
            return "Slow Down"
        if "continue" in normalized:
            return "Continue"
        return "Slow Down"

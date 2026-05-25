from dataclasses import dataclass

POSITIVE = {"stabilize", "improved", "growth", "recover", "secure"}
NEGATIVE = {"strike", "shutdown", "recall", "conflict", "delay", "bankruptcy"}


@dataclass
class NLPResult:
    sentiment: float
    risk_adjustment: float
    summary: str


class NLPService:
    def analyze(self, headlines: list[str]) -> NLPResult:
        if not headlines:
            return NLPResult(0.0, 0.0, "No external signals")
        score = 0
        for h in headlines:
            tokens = set(h.lower().split())
            score += len(tokens & POSITIVE)
            score -= len(tokens & NEGATIVE)
        sentiment = score / max(len(headlines), 1)
        adjustment = max(min(-0.05 * sentiment, 0.2), -0.2)
        return NLPResult(sentiment, adjustment, f"Analyzed {len(headlines)} headlines")

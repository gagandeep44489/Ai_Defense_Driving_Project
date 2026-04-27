"""NLP-based risk signal extraction from headlines."""
from __future__ import annotations

from typing import Dict, List


NEGATIVE_TERMS = {
    "strike",
    "shutdown",
    "recall",
    "bankruptcy",
    "shortage",
    "war",
    "sanction",
    "delay",
    "defect",
    "crisis",
    "inflation",
    "disruption",
    "accident",
    "fire",
}

POSITIVE_TERMS = {
    "expansion",
    "investment",
    "partnership",
    "award",
    "growth",
    "improvement",
    "stable",
    "recovery",
    "innovation",
}


def analyze_headline_sentiment(headline: str) -> float:
    """Lexicon-based sentiment score in range [-1, 1]."""
    tokens = [token.strip(".,!?:;()[]{}\"'").lower() for token in headline.split()]
    if not tokens:
        return 0.0

    neg_hits = sum(1 for t in tokens if t in NEGATIVE_TERMS)
    pos_hits = sum(1 for t in tokens if t in POSITIVE_TERMS)

    raw = (pos_hits - neg_hits) / max(len(tokens), 1)
    return max(-1.0, min(1.0, raw * 5.0))


def news_risk_score(headlines: List[str]) -> Dict:
    """Aggregate news sentiment into a risk adjustment score [0, 1]."""
    if not headlines:
        return {
            "headline_scores": [],
            "sentiment_mean": 0.0,
            "news_risk": 0.0,
            "summary": "No headlines provided",
        }

    per_headline = []
    for h in headlines:
        score = analyze_headline_sentiment(h)
        per_headline.append({"headline": h, "sentiment": round(score, 4)})

    mean_sentiment = sum(item["sentiment"] for item in per_headline) / len(per_headline)
    # Negative sentiment increases risk, positive sentiment decreases it.
    risk = max(0.0, min(1.0, (-mean_sentiment + 1.0) / 2.0))

    if mean_sentiment < -0.2:
        summary = "Negative external risk signals detected"
    elif mean_sentiment > 0.2:
        summary = "Mostly positive external signals"
    else:
        summary = "Neutral external risk signals"

    return {
        "headline_scores": per_headline,
        "sentiment_mean": round(mean_sentiment, 4),
        "news_risk": round(risk, 4),
        "summary": summary,
    }


def combine_model_and_news_risk(model_label: str, news_risk: float) -> Dict:
    """Fuse classifier risk level with NLP risk score."""
    base_map = {"Low": 0.25, "Medium": 0.6, "High": 0.9}
    base_score = base_map.get(model_label, 0.5)
    combined_score = max(0.0, min(1.0, 0.75 * base_score + 0.25 * news_risk))

    if combined_score >= 0.75:
        fused_label = "High"
    elif combined_score >= 0.45:
        fused_label = "Medium"
    else:
        fused_label = "Low"

    return {
        "model_score": round(base_score, 4),
        "combined_score": round(combined_score, 4),
        "final_risk": fused_label,
    }

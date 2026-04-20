from __future__ import annotations

import json

from services.llm_service import llm_service


async def generate_insights_with_llm(metrics: dict) -> str:
    prompt = (
        "Analyze the following hospital metrics and generate a concise weekly report "
        "highlighting trends, risks, and recommendations. "
        "Only use aggregate-level language and no patient-identifiable information.\n\n"
        f"Metrics JSON:\n{json.dumps(metrics, indent=2)}"
    )
    text = await llm_service.generate_text(prompt, temperature=0.2)

    if text.startswith("LLM API key not configured"):
        high_pct = metrics.get("risk_distribution", {}).get("high_pct", 0)
        overloaded = metrics.get("workload_summary", {}).get("overloaded_doctors", 0)
        return (
            "AI-assisted insights: Weekly trend indicates "
            f"{high_pct}% high-risk patients with {overloaded} overloaded doctors. "
            "Recommend balancing schedules and prioritizing high-risk follow-ups."
        )

    if not text.lower().startswith("ai-assisted insights"):
        return f"AI-assisted insights: {text}"
    return text

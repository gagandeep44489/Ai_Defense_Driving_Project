"""Agent confidence/agreement visualizations for Saarthi UI."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List

import streamlit as st


def render_agent_graphs(agent_outputs: List[Dict], final_decision: str) -> Dict[str, float]:
    st.markdown("<div class='card'><b>📊 Agent Analysis Dashboard</b><div class='card-sub'>Confidence and consensus diagnostics</div></div>", unsafe_allow_html=True)

    if not agent_outputs:
        st.info("No agent output data available.")
        return {"agreement_score": 0.0}

    # Row 1: confidence bar chart
    st.markdown("**Confidence by Agent (%)**")
    confidence_rows = {row["agent"]: row["confidence"] for row in agent_outputs}
    st.bar_chart(confidence_rows, use_container_width=True)

    # Row 2: decision distribution (horizontal bar simulated with sorted bar chart)
    st.markdown("**Decision Distribution (Agent Votes)**")
    decision_counts = Counter(row.get("decision", "Unknown") for row in agent_outputs)
    st.bar_chart(dict(decision_counts), use_container_width=True)

    # Row 3: agreement + weighted confidence decision
    supporting = sum(1 for row in agent_outputs if row.get("decision") == final_decision)
    total = len(agent_outputs)
    agreement_score = round((supporting / total) * 100, 1) if total else 0.0

    weighted = defaultdict(int)
    for row in agent_outputs:
        weighted[row.get("decision", "Unknown")] += int(row.get("confidence", 0))

    weighted_winner = max(weighted, key=weighted.get)
    c1, c2 = st.columns(2)
    c1.metric("Agreement Score", f"{agreement_score}%")
    c2.metric("Confidence-Weighted Winner", f"{weighted_winner} ({weighted[weighted_winner]})")

    if agreement_score < 60:
        st.warning("High disagreement detected among agents.")
    else:
        st.success("Strong consensus among agents.")

    return {
        "agreement_score": agreement_score,
        "supporting_agents": supporting,
        "total_agents": total,
        "weighted_winner": weighted_winner,
    }

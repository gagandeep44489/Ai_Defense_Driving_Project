"""Debate chat visualization for Saarthi AI Streamlit UI."""

from __future__ import annotations

import time
from typing import Dict

import streamlit as st


AGENT_STYLES = {
    "RiskAgent": {"side": "left", "label": "🟥 RiskAgent", "class": "bubble-risk"},
    "SafetyAgent": {"side": "right", "label": "🟩 SafetyAgent", "class": "bubble-safety"},
    "IntentAgent": {"side": "left", "label": "🟦 IntentAgent", "class": "bubble-intent"},
    "EfficiencyAgent": {"side": "right", "label": "🟨 EfficiencyAgent", "class": "bubble-eff"},
    "Consensus": {"side": "left", "label": "✅ Consensus", "class": "bubble-consensus"},
}


def render_debate(debate_result: Dict, animate: bool = False) -> None:
    st.markdown("<div class='card'><b>🧠 Agent Debate</b><div class='card-sub'>Stepwise multi-agent argument flow</div></div>", unsafe_allow_html=True)

    for entry in debate_result.get("debate", []):
        agent = entry.get("agent", "RiskAgent")
        style = AGENT_STYLES.get(agent, AGENT_STYLES["RiskAgent"])
        step = entry.get("step", "?")
        confidence = entry.get("confidence")
        conf_text = f" | confidence: {confidence}" if confidence is not None else ""

        bubble_html = (
            f"<div class='debate-row {style['side']}'>"
            f"<div class='debate-bubble {style['class']}'><b>Step {step} · {style['label']}</b><br>{entry.get('message', '')}{conf_text}</div>"
            "</div>"
        )
        st.markdown(bubble_html, unsafe_allow_html=True)
        if animate:
            time.sleep(0.08)

    winning = debate_result.get("winning_argument_agent", "RiskAgent")
    final_decision = debate_result.get("final_decision", "Slow Down")
    st.markdown(
        f"<div class='card'><b>🏁 FINAL DECISION:</b> {final_decision}<br><span class='card-sub'>Winning argument: {winning}</span></div>",
        unsafe_allow_html=True,
    )

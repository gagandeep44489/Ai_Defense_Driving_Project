"""Mobile-style Saarthi AI Streamlit infotainment interface."""

from __future__ import annotations

import json
import random
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from agents.debate_engine import DebateEngine
from agents.llm_reasoner import LLMReasoner
from map.map_engine import build_deck
from map.objects import objects_for_scenario
from map.routes import adjust_route_for_decision, route_for_scenario
from main import SCENARIOS, run
from ui.components import (
    alert_card_html,
    decision_card_html,
    intent_card_html,
    live_drive_card_html,
    status_bar_html,
)
from ui.debate_view import render_debate
from ui.graphs import render_agent_graphs
from voice.tts import build_alert_text, speak


st.set_page_config(page_title="Saarthi AI Mobile UI", page_icon="🚗", layout="centered")

SCENARIO_MAP = {
    "Pothole + Bus Behind": 1,
    "Stray Dog Crossing": 2,
    "Wrong-side Bike": 3,
}
LANGUAGE_MAP = {"Hindi": "hi", "Punjabi": "pa"}


def load_css() -> None:
    css = Path("ui/styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_bottom_nav() -> None:
    st.markdown("---")
    cols = st.columns(4)
    tabs = ["🏠 Home", "🚗 Simulation", "🗺️ Live Map", "⚙️ Settings"]
    for idx, tab in enumerate(tabs):
        if cols[idx].button(tab, use_container_width=True):
            st.session_state.active_tab = tab
    st.markdown(f"<div class='nav-note'>Active Tab: {st.session_state.active_tab}</div>", unsafe_allow_html=True)


def init_state() -> None:
    st.session_state.setdefault("result", None)
    st.session_state.setdefault("debate_result", None)
    st.session_state.setdefault("voice_alert_text", "")
    st.session_state.setdefault("voice_triggered", False)
    st.session_state.setdefault("active_tab", "🚗 Simulation")


def run_simulation(selected_scenario: str, selected_language: str, save_output_json: bool) -> None:
    scenario_id = SCENARIO_MAP[selected_scenario]
    with st.spinner("AI is thinking..."):
        progress = st.progress(0, text="Scanning environment...")
        for pct in (10, 25, 45, 65, 85, 100):
            time.sleep(0.08)
            progress.progress(pct, text="Scanning environment...")

        st.session_state.result = run(
            scenario=SCENARIOS[scenario_id],
            model_name="microsoft/phi-3-mini-4k-instruct",
            use_mock=False,
        )

    debate_reasoner = LLMReasoner(
        model_name="microsoft/phi-3-mini-4k-instruct",
        use_mock=st.session_state.result.get("used_fallback", True),
    )
    debate_engine = DebateEngine(debate_reasoner)
    st.session_state.debate_result = debate_engine.run_debate(
        scenario_input=SCENARIOS[scenario_id],
        base_result=st.session_state.result,
    )
    st.session_state.result["decision"] = st.session_state.debate_result["final_decision"]

    lang_code = LANGUAGE_MAP[selected_language]
    alert_text = build_alert_text(
        decision=st.session_state.result["decision"],
        risk=st.session_state.result["risk"],
        objects=st.session_state.result["objects"],
        lang=lang_code,
    )
    speak(alert_text, lang=lang_code, rate=150, include_beep=True)
    st.session_state.voice_alert_text = alert_text
    st.session_state.voice_triggered = True

    if save_output_json:
        output_dir = Path("outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"mobile_ui_scenario_{scenario_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        filename.write_text(json.dumps(st.session_state.result, indent=2), encoding="utf-8")
        st.toast(f"Saved output: {filename}")


def main() -> None:
    load_css()
    init_state()

    st.markdown("<div class='mobile-shell'>", unsafe_allow_html=True)
    st.markdown(status_bar_html(), unsafe_allow_html=True)
    st.markdown("<div class='app-title'><b>Saarthi AI</b></div>", unsafe_allow_html=True)

    selected_scenario = st.selectbox("Scenario", list(SCENARIO_MAP.keys()), label_visibility="collapsed")
    selected_language = st.segmented_control("Language", options=["Hindi", "Punjabi"], default="Hindi")
    save_output_json = st.toggle("Save Output JSON", value=False)

    if st.button("Start Drive", use_container_width=True, type="primary"):
        run_simulation(selected_scenario, selected_language, save_output_json)

    if st.session_state.result is None:
        st.markdown("<div class='card'>Tap <b>Start Drive</b> to begin simulation.</div>", unsafe_allow_html=True)
        render_bottom_nav()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    result = st.session_state.result
    debate_result = st.session_state.debate_result
    dashboard_tab, map_tab = st.tabs(["🚗 Dashboard", "🗺️ Live Map"])

    with dashboard_tab:
        st.markdown(live_drive_card_html(result["scenario"]["name"], result["risk"]), unsafe_allow_html=True)
        st.markdown(alert_card_html(st.session_state.voice_alert_text, result["risk"]), unsafe_allow_html=True)
        st.markdown(decision_card_html(result["decision"]), unsafe_allow_html=True)
        st.markdown(intent_card_html(result["intent"]), unsafe_allow_html=True)

        if st.session_state.voice_triggered:
            st.success("🔊 Voice Alert Triggered")
            st.caption(f"Subtitle: {st.session_state.voice_alert_text}")

        with st.expander("📜 View AI Reasoning"):
            for step in result["thought_log"]:
                st.markdown(f"→ {step}")

        if debate_result is not None:
            render_debate(debate_result, animate=True)
            render_agent_graphs(
                debate_result.get("agent_outputs", []),
                final_decision=debate_result.get("final_decision", result["decision"]),
            )

        st.markdown(
            f"<div class='card'><b>System:</b> AI Active | <b>Latency:</b> {result['latency_seconds']}s | <b>Model:</b> Phi-3</div>",
            unsafe_allow_html=True,
        )

    with map_tab:
        st.markdown("<div class='card'><b>🗺️ Live Map Simulation</b><div class='card-sub'>AI-driven route adaptation</div></div>", unsafe_allow_html=True)
        sim_speed = st.slider("Simulation Speed", min_value=1, max_value=5, value=3, help="Higher is faster movement")
        start_map = st.button("Start Map Simulation", use_container_width=True)

        if start_map:
            scenario_id = SCENARIO_MAP[selected_scenario]
            # Ensure AI decision exists before map animation.
            if st.session_state.result is None or st.session_state.result["scenario"]["id"] != scenario_id:
                run_simulation(selected_scenario, selected_language, save_output_json=False)
                result = st.session_state.result

            raw_route = route_for_scenario(scenario_id)
            route = adjust_route_for_decision(raw_route, result["decision"])
            objects = objects_for_scenario(scenario_id)

            map_placeholder = st.empty()
            status_placeholder = st.empty()
            step_sleep = max(0.08, 0.4 - (sim_speed * 0.06))

            for idx, point in enumerate(route):
                jitter = [point[0] + random.uniform(-0.00003, 0.00003), point[1] + random.uniform(-0.00003, 0.00003)]
                deck = build_deck(route, jitter, objects, result["risk"])
                map_placeholder.pydeck_chart(deck, use_container_width=True)
                status_placeholder.info(
                    f"Step {idx + 1}/{len(route)} • Decision: {result['decision']} • Risk: {result['risk']} • AI Intervention Active"
                )
                time.sleep(step_sleep)

            st.success("Navigation simulation complete.")

    render_bottom_nav()
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

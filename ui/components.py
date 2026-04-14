"""Reusable UI components for Saarthi mobile dashboard."""

from __future__ import annotations

from datetime import datetime
from typing import Dict


def status_bar_html() -> str:
    now = datetime.now().strftime("%H:%M")
    return (
        "<div class='status-bar'>"
        f"<span>{now}</span>"
        "<span>📶 4G</span>"
        "<span>🔋 87%</span>"
        "</div>"
    )


def live_drive_card_html(scenario_name: str, risk: str) -> str:
    status = "Risk Detected" if risk in {"High", "Medium"} else "Driving"
    return (
        "<div class='card'>"
        "<div><span class='blink-dot'></span><b>🚗 LIVE DRIVE</b></div>"
        f"<div style='margin-top:6px;'>Scenario: <b>{scenario_name}</b></div>"
        f"<div class='card-sub'>Status: {status}</div>"
        "</div>"
    )


def alert_card_html(alert_text: str, risk: str) -> str:
    risk_class = "alert-high" if risk == "High" else "alert-medium" if risk == "Medium" else "alert-low"
    return (
        f"<div class='card {risk_class}'>"
        "<div class='card-sub'>⚠️ AI ALERT</div>"
        f"<div class='big-alert'>{alert_text}</div>"
        f"<div class='card-sub'>Risk Level: {risk}</div>"
        "</div>"
    )


def decision_card_html(decision: str) -> str:
    return (
        "<div class='card'>"
        "<div><b>🧠 DECISION</b></div>"
        f"<div style='font-size:1.2rem;font-weight:800;margin-top:6px;'>{decision}</div>"
        "<div class='card-sub'>AI Intervention Active</div>"
        "</div>"
    )


def intent_card_html(intent_map: Dict[str, str]) -> str:
    rows = "".join(
        f"<div style='margin-top:6px;'><b>{obj.title()}</b> → {intent}</div>" for obj, intent in intent_map.items()
    )
    if not rows:
        rows = "<div class='card-sub'>No intent entries</div>"
    return (
        "<div class='card'>"
        "<div><b>📊 INTENT</b></div>"
        f"{rows}"
        "</div>"
    )

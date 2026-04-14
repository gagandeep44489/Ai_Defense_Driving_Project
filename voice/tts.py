"""Offline text-to-speech helpers for Saarthi AI voice alerts."""

from __future__ import annotations

import threading
from typing import Optional


def _select_voice(engine, lang: str) -> None:
    """Pick best available voice for Hindi/Punjabi if present."""
    target_tokens = {
        "hi": ["hindi", "hi", "india"],
        "pa": ["punjabi", "pa", "india"],
    }.get(lang, ["hindi", "india"])

    selected_id: Optional[str] = None
    for voice in engine.getProperty("voices"):
        sample = f"{getattr(voice, 'id', '')} {getattr(voice, 'name', '')}".lower()
        langs = " ".join(str(x).lower() for x in getattr(voice, "languages", []))
        haystack = f"{sample} {langs}"
        if any(token in haystack for token in target_tokens):
            selected_id = voice.id
            break

    if selected_id:
        engine.setProperty("voice", selected_id)


def _speak_worker(text: str, lang: str, rate: int, include_beep: bool) -> None:
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        _select_voice(engine, lang)

        if include_beep:
            print("\a", end="")

        engine.say(text)
        engine.runAndWait()
    except Exception:
        # Silent fail keeps UI responsive in environments without audio support.
        return


def speak(text: str, lang: str = "hi", rate: int = 150, include_beep: bool = True) -> threading.Thread:
    """Speak alert text asynchronously so Streamlit UI is not blocked."""
    worker = threading.Thread(
        target=_speak_worker,
        kwargs={"text": text, "lang": lang, "rate": rate, "include_beep": include_beep},
        daemon=True,
    )
    worker.start()
    return worker


def build_alert_text(decision: str, risk: str, objects: list[str], lang: str = "hi") -> str:
    """Map decision/risk/object state to Hindi/Punjabi voice alerts."""
    is_dog = any(obj.lower() == "animal" for obj in objects)
    has_vehicle = any(obj.lower() in {"car", "bus", "bike", "wrong-side vehicle"} for obj in objects)

    if lang == "pa":
        if decision == "Brake":
            if is_dog:
                return "Brake! Kutta agge aa gaya!"
            if has_vehicle:
                return "Brake! Gaddi saamne hai!"
            return "Brake! Turant sambhal ke!"
        if decision in {"Avoid", "Avoid pothole without hard braking"}:
            return "Side ton nikal rahe haan, dhyaan rakho!"
        if risk == "High":
            return "Danger! Sambhal ke chalao!"
        return "Road clear hai, par satark raho."

    # Default Hindi
    if decision == "Brake":
        if is_dog:
            return "Brake! Kutta aa gaya!"
        if has_vehicle:
            return "Brake! Gaadi saamne hai!"
        return "Brake! Turant sambhaliye!"
    if decision in {"Avoid", "Avoid pothole without hard braking"}:
        return "Side se nikal rahe hain, dhyaan rakho!"
    if risk == "High":
        return "Danger! Sambhal ke chalao!"
    return "Raasta theek hai, par satark rahiye."

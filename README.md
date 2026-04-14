# Saarthi AI – LLM-Powered Agentic Defensive Driving System

Saarthi AI is an offline, explainable driving-reasoning simulator tailored for Indian road complexity. It upgrades a rule-based pipeline into a **local Small Language Model (SLM)** reasoning engine that produces transparent decisions and a full thought log.

## Why this matters (Indian roads)

Indian roads often include:
- mixed traffic behavior,
- sudden potholes,
- stray animals,
- heavy vehicles tailgating,
- wrong-side two-wheelers.

These cases are hard to model with static rules. LLM reasoning provides better contextual judgment and richer explanations.

## LLM-first architecture

```text
Scenario Input
   |
   v
PerceptionAgent (extract objects)
   |
   v
LLMReasoner (local Phi-3/Llama prompt + JSON reasoning)
   |
   v
DecisionAgent (normalize safe action labels)
   |
   v
ThoughtLogger (thought log + latency + fallback flag + JSON save)
```

## Project structure

```text
/project-root
│── main.py
│── agents/
│     ├── perception.py
│     ├── llm_reasoner.py
│     ├── decision.py
│     ├── logger.py
│── scenarios/
│     ├── scenario1.py
│     ├── scenario2.py
│     ├── scenario3.py
│── utils/
│     ├── prompt_templates.py
│── requirements.txt
│── README.md
```

## Model choices

Default: `microsoft/phi-3-mini-4k-instruct`  
Alternative (if resources allow): `meta-llama/Meta-Llama-3-8B-Instruct`

> The code uses `local_files_only=True` to support offline inference with locally cached/downloaded weights.

## Prompt contract

The LLM is forced to output strict JSON:

```json
{
  "objects": [],
  "intent": {},
  "risk": "",
  "decision": "",
  "thought_log": []
}
```

## Scenarios included

1. pothole + bus behind
2. stray dog crossing
3. wrong-side bike coming

## Run locally

### 1) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run a scenario

```bash
python main.py --scenario 1
```

### 3) Deterministic fallback mode (no model load)

```bash
python main.py --scenario 1 --mock
```

### 4) JSON output + save

```bash
python main.py --scenario 2 --json --save-json outputs/scenario2.json
```

## Run UI Dashboard

Launch the in-vehicle style Streamlit interface:

```bash
streamlit run app.py
```

Dashboard features:
- scenario selector and one-click simulation,
- language selector (Hindi/Punjabi),
- live "AI is thinking..." spinner + scan progress,
- environment metrics (objects, distances, speeds),
- decision + color-coded risk panel,
- intent table,
- timeline-style thought log,
- system status (model, latency, AI active),
- optional JSON save from sidebar toggle,
- real-time offline voice alerts with subtitle text.

## Mobile UI Experience

The dashboard now mimics a **mobile in-car infotainment screen**:
- centered mobile-shell layout (~400px feeling) for realistic cockpit storytelling,
- dark high-contrast theme with rounded cards and shadows,
- top status bar (time, network, battery),
- touch-first controls inside main UI (scenario, language, Start Drive),
- live drive card, AI alert card, decision card, intent card,
- expandable thought log,
- bottom navigation tabs (`Home / Simulation / Analytics / Settings`).

UI assets:
- `ui/styles.css` for custom dark theme and animations (including blinking risk dot),
- `ui/components.py` for reusable card/status HTML components.

## Live Map Simulation

Saarthi now includes a **Google Maps–style live simulation tab** (`🗺️ Live Map`) in the Streamlit app:
- map centered on Punjab region (`31.1471, 75.3412`),
- animated vehicle movement over route points,
- obstacle overlays (dog, pothole, bike, bus),
- AI decision-aware route behavior:
  - `Brake` → shorter/slow movement,
  - `Avoid` → slight lane-shift path,
  - `Turn` → directional route change,
  - `Continue` → normal path.

Implementation modules:
- `map/routes.py` for route generation + decision-based path adjustment,
- `map/objects.py` for scenario map entities,
- `map/map_engine.py` for Pydeck layers (`ScatterplotLayer`, `PathLayer`) and deck rendering.

## Multi-Agent Debate Visualization

Saarthi now includes an **Agent Debate** module where four agents argue before final decision sync:
- `RiskAgent` (collision probability),
- `SafetyAgent` (passenger protection),
- `IntentAgent` (behavior prediction),
- `EfficiencyAgent` (smooth/time-efficient driving).

Debate flow:
1. initial arguments,
2. counter-arguments,
3. consensus decision.

Implementation:
- `agents/debate_engine.py` runs structured debate rounds and returns a consensus decision + confidence metadata.
- `ui/debate_view.py` renders chat-style left/right bubbles with agent colors and a highlighted final decision card.
- `ui/graphs.py` renders confidence bars, decision distribution, agreement score, confidence-weighted winner, and consensus insight text.

## Voice Assistant

Saarthi AI now includes a non-blocking offline voice assistant powered by `pyttsx3`.

- Module: `voice/tts.py`
- API: `speak(text, lang=\"hi\")`
- Supported alert languages:
  - Hindi
  - Punjabi
- Trigger behavior:
  - Brake + dog: `Brake! Kutta aa gaya!`
  - Brake + vehicle: `Brake! Gaadi saamne hai!`
  - Avoid: `Side se nikal rahe hain, dhyaan rakho!`
  - High risk: `Danger! Sambhal ke chalao!`

Install requirement:

```bash
pip install pyttsx3
```

## Example thought log

```text
[Thought Log]
- Pothole detected ahead.
- Bus is following closely from behind.
- Hard braking may trigger rear-end collision.
- Controlled lane adjustment is safer.
```

## Notes

- CPU-friendly design with small models.
- No external APIs.
- Includes fallback reasoning if model parsing/inference fails.
- Includes latency measurement for hackathon demos.

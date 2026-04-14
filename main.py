"""Entrypoint for Saarthi AI LLM-powered defensive driving simulation."""

from __future__ import annotations

import argparse
import json

from agents.decision import DecisionAgent
from agents.llm_reasoner import LLMReasoner
from agents.logger import ThoughtLogger
from agents.perception import PerceptionAgent

from scenarios.scenario1 import SCENARIO as SCENARIO_1
from scenarios.scenario2 import SCENARIO as SCENARIO_2
from scenarios.scenario3 import SCENARIO as SCENARIO_3


SCENARIOS = {1: SCENARIO_1, 2: SCENARIO_2, 3: SCENARIO_3}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Saarthi AI - LLM Defensive Driving")
    parser.add_argument("--scenario", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--model", type=str, default="microsoft/phi-3-mini-4k-instruct")
    parser.add_argument("--mock", action="store_true", help="Use deterministic fallback reasoning without loading a model")
    parser.add_argument("--json", action="store_true", help="Print strict JSON output")
    parser.add_argument("--save-json", type=str, default="", help="Optional file path to save output JSON")
    return parser.parse_args()


def run(scenario: dict, model_name: str, use_mock: bool) -> dict:
    perception = PerceptionAgent()
    reasoner = LLMReasoner(model_name=model_name, use_mock=use_mock)
    decision_agent = DecisionAgent()
    logger = ThoughtLogger()

    detected_objects = perception.detect(scenario)
    llm_input = {**scenario, "objects": detected_objects}

    result = reasoner.reason(llm_input)
    payload = result.payload
    payload["decision"] = decision_agent.finalize(payload)
    logger.extend(payload.get("thought_log", []))

    return logger.build_record(scenario, payload, result.latency_seconds, result.used_fallback)


def print_human_readable(record: dict) -> None:
    print(f"=== Saarthi AI | Scenario {record['scenario']['id']}: {record['scenario']['name']} ===")
    print(f"Detected objects: {', '.join(record['objects'])}")
    print("Intent predictions:")
    for obj, intent in record["intent"].items():
        print(f"- {obj}: {intent}")
    print(f"Risk level: {record['risk']}")
    print(f"Final decision: {record['decision']}")
    print(f"Latency: {record['latency_seconds']}s")
    print(f"Fallback used: {record['used_fallback']}")
    print("\n[Thought Log]")
    for step in record["thought_log"]:
        print(f"- {step}")


def main() -> None:
    args = parse_args()
    scenario = SCENARIOS[args.scenario]
    record = run(scenario, model_name=args.model, use_mock=args.mock)

    if args.save_json:
        ThoughtLogger().save_json(args.save_json, record)

    if args.json:
        print(json.dumps(record, indent=2))
    else:
        print_human_readable(record)


if __name__ == "__main__":
    main()

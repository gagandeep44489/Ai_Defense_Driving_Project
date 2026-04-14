"""Multi-agent debate engine for Saarthi AI decision transparency."""

from __future__ import annotations

import time
from typing import Any, Dict, List


class DebateEngine:
    """Runs a structured debate among Risk/Safety/Intent/Efficiency agents."""

    AGENTS = ["RiskAgent", "SafetyAgent", "IntentAgent", "EfficiencyAgent"]

    def __init__(self, llm_reasoner) -> None:
        self.reasoner = llm_reasoner

    def run_debate(self, scenario_input: Dict[str, Any], base_result: Dict[str, Any]) -> Dict[str, Any]:
        initial_round: List[Dict[str, Any]] = []
        agent_outputs: List[Dict[str, Any]] = []
        for agent in self.AGENTS:
            msg = self._agent_statement(agent, scenario_input, base_result, round_type="initial")
            confidence = self._confidence(agent, base_result)
            decision_hint = self._infer_decision_from_message(msg, base_result.get("decision", "Slow Down"))
            initial_round.append(
                {
                    "step": 1,
                    "agent": agent,
                    "message": msg,
                    "confidence": confidence,
                    "decision": decision_hint,
                }
            )
            agent_outputs.append(
                {
                    "agent": agent,
                    "confidence": int(round(confidence * 100)),
                    "decision": decision_hint,
                }
            )

        prior_context = " ".join(item["message"] for item in initial_round)
        counter_round: List[Dict[str, Any]] = []
        for agent in self.AGENTS:
            msg = self._agent_statement(agent, scenario_input, base_result, round_type="counter", context=prior_context)
            counter_round.append(
                {
                    "step": 2,
                    "agent": agent,
                    "message": msg,
                    "confidence": self._confidence(agent, base_result) - 0.03,
                    "decision": self._infer_decision_from_message(msg, base_result.get("decision", "Slow Down")),
                }
            )

        votes = self._vote(initial_round + counter_round, base_result)
        final_decision = max(votes, key=votes.get)
        winner = self._winning_agent(initial_round + counter_round)

        consensus = {
            "step": 3,
            "agent": "Consensus",
            "message": f"Final consensus after debate: {final_decision}",
        }

        return {
            "debate": initial_round + counter_round + [consensus],
            "final_decision": final_decision,
            "winning_argument_agent": winner,
            "votes": votes,
            "agent_outputs": agent_outputs,
            "generated_at": round(time.time(), 3),
        }

    def _agent_statement(
        self,
        agent: str,
        scenario_input: Dict[str, Any],
        base_result: Dict[str, Any],
        round_type: str,
        context: str = "",
    ) -> str:
        if self.reasoner.use_mock or self.reasoner.model is None or self.reasoner.tokenizer is None:
            return self._fallback_statement(agent, base_result, round_type)

        prompt = (
            f"You are {agent}. Analyze this Indian-road scenario and argue your position. "
            f"Round: {round_type}. "
            f"Current AI decision: {base_result.get('decision')}. "
            f"Risk: {base_result.get('risk')}. "
            f"Objects: {base_result.get('objects')}. "
            f"Intent map: {base_result.get('intent')}. "
            f"Other agents so far: {context[:350]} "
            "Give one concise argument sentence."
        )
        try:
            model_input = self.reasoner.tokenizer(prompt, return_tensors="pt")
            output_ids = self.reasoner.model.generate(
                **model_input,
                do_sample=True,
                temperature=0.3,
                max_new_tokens=80,
            )
            text = self.reasoner.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            return text[-220:].strip() if text else self._fallback_statement(agent, base_result, round_type)
        except Exception:
            return self._fallback_statement(agent, base_result, round_type)

    def _fallback_statement(self, agent: str, base_result: Dict[str, Any], round_type: str) -> str:
        decision = base_result.get("decision", "Slow Down")
        risk = base_result.get("risk", "Medium")
        objects = set(base_result.get("objects", []))

        if agent == "RiskAgent":
            return (
                "Rear collision risk is high if we brake abruptly."
                if {"bus", "car"} & objects
                else f"Primary collision probability remains {risk.lower()}, so we need a defensive trajectory."
            )
        if agent == "SafetyAgent":
            return (
                "Passenger safety comes first; prefer controlled speed reduction and stable steering."
                if round_type == "initial"
                else "I challenge aggressive actions; controlled maneuvering lowers injury risk."
            )
        if agent == "IntentAgent":
            return (
                "Nearby road users may behave unpredictably, especially animals and wrong-side vehicles."
                if round_type == "initial"
                else "Given probable intent shifts, keep buffer distance and avoid sudden jerks."
            )
        return (
            f"Efficiency supports '{decision}' because it balances smooth flow with safety margins."
            if round_type == "initial"
            else "I support the option with minimal delay while preserving safe lane discipline."
        )

    def _vote(self, messages: List[Dict[str, Any]], base_result: Dict[str, Any]) -> Dict[str, int]:
        options = {
            "Brake": 0,
            "Slow Down": 0,
            "Avoid": 0,
            "Turn": 0,
            "Continue": 0,
        }
        text_blob = " ".join(msg["message"].lower() for msg in messages)
        if "turn" in text_blob or "wrong-side" in text_blob:
            options["Turn"] += 2
        if "avoid" in text_blob or "maneuver" in text_blob:
            options["Avoid"] += 2
        if "slow" in text_blob or "controlled" in text_blob:
            options["Slow Down"] += 2
        if "brake" in text_blob:
            options["Brake"] += 1
        if "continue" in text_blob:
            options["Continue"] += 1

        base_decision = base_result.get("decision", "Slow Down")
        normalized = "Avoid" if "avoid" in base_decision.lower() else base_decision
        options[normalized] = options.get(normalized, 0) + 3
        return options

    def _winning_agent(self, messages: List[Dict[str, Any]]) -> str:
        scored = [(m.get("confidence", 0), m.get("agent", "")) for m in messages if m.get("agent") in self.AGENTS]
        if not scored:
            return "RiskAgent"
        scored.sort(reverse=True)
        return scored[0][1]

    def _confidence(self, agent: str, base_result: Dict[str, Any]) -> float:
        risk = base_result.get("risk", "Medium")
        base = 0.72 if risk == "High" else 0.64 if risk == "Medium" else 0.58
        offsets = {"RiskAgent": 0.08, "SafetyAgent": 0.06, "IntentAgent": 0.05, "EfficiencyAgent": 0.04}
        return round(min(0.98, base + offsets.get(agent, 0.04)), 2)

    def _infer_decision_from_message(self, message: str, default: str) -> str:
        text = message.lower()
        if "turn" in text:
            return "Turn"
        if "avoid" in text or "maneuver" in text:
            return "Avoid"
        if "brake" in text:
            return "Brake"
        if "slow" in text or "controlled" in text:
            return "Slow Down"
        if "continue" in text:
            return "Continue"
        return "Avoid" if "avoid" in default.lower() else default

"""LLM-powered reasoning agent for Saarthi AI."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from utils.prompt_templates import build_reasoning_prompt


@dataclass
class ReasoningResult:
    payload: Dict[str, Any]
    latency_seconds: float
    used_fallback: bool


class LLMReasoner:
    """Runs local SLM inference and parses strict JSON outputs."""

    def __init__(
        self,
        model_name: str = "microsoft/phi-3-mini-4k-instruct",
        device: Optional[str] = None,
        use_mock: bool = False,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.use_mock = use_mock
        self.model = None
        self.tokenizer = None

        if not self.use_mock:
            try:
                self._load_model()
            except Exception:
                self.use_mock = True

    def _load_model(self) -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            local_files_only=True,
            torch_dtype="auto",
            device_map=self.device or "auto",
        )

    def reason(self, scenario: Dict[str, Any]) -> ReasoningResult:
        start = time.perf_counter()
        prompt = build_reasoning_prompt(scenario)

        if self.use_mock or self.model is None or self.tokenizer is None:
            payload = self._fallback_reasoning(scenario)
            return ReasoningResult(payload=payload, latency_seconds=time.perf_counter() - start, used_fallback=True)

        try:
            model_input = self.tokenizer(prompt, return_tensors="pt")
            output_ids = self.model.generate(
                **model_input,
                do_sample=True,
                temperature=0.3,
                max_new_tokens=300,
            )
            text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            payload = self._parse_json_from_text(text)
            payload = self._normalize_payload(payload, scenario)
            return ReasoningResult(payload=payload, latency_seconds=time.perf_counter() - start, used_fallback=False)
        except Exception:
            payload = self._fallback_reasoning(scenario)
            return ReasoningResult(payload=payload, latency_seconds=time.perf_counter() - start, used_fallback=True)

    def _parse_json_from_text(self, text: str) -> Dict[str, Any]:
        if text.strip().startswith("{"):
            return json.loads(text)

        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in model output")

        return json.loads(match.group(0))

    def _normalize_payload(self, payload: Dict[str, Any], scenario: Dict[str, Any]) -> Dict[str, Any]:
        objects = payload.get("objects") or [obj["type"] for obj in scenario.get("objects", [])]
        intent = payload.get("intent") or {}
        risk = payload.get("risk") or "Medium"
        decision = payload.get("decision") or "Slow Down"
        thought_log = payload.get("thought_log") or ["Model returned incomplete output; applied safe defaults."]

        return {
            "objects": objects,
            "intent": intent,
            "risk": risk,
            "decision": decision,
            "thought_log": thought_log,
        }

    def _fallback_reasoning(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        object_types = [obj["type"] for obj in scenario.get("objects", [])]
        intent: Dict[str, str] = {}

        for obj in scenario.get("objects", []):
            obj_type = obj["type"]
            if obj_type == "bus" and obj.get("position") == "behind":
                intent[obj_type] = "may not slow down quickly"
            elif obj_type == "animal":
                intent[obj_type] = "may suddenly cross path"
            elif obj_type == "wrong-side vehicle" or obj.get("direction") == "wrong-side":
                intent[obj_type] = "likely to continue against traffic"
            elif obj_type == "pothole":
                intent[obj_type] = "stationary hazard requiring lane adjustment"
            else:
                intent[obj_type] = "likely to maintain current movement"

        if "wrong-side vehicle" in object_types:
            risk, decision = "High", "Turn"
            thought = [
                "Wrong-side vehicle detected ahead.",
                "Head-on conflict risk is high.",
                "Safer action is to change path and create lateral clearance.",
            ]
        elif "animal" in object_types:
            risk, decision = "High", "Slow Down"
            thought = [
                "Animal is near lane boundary.",
                "Animal motion is unpredictable.",
                "Reducing speed provides reaction buffer.",
            ]
        elif "pothole" in object_types and "bus" in object_types:
            risk, decision = "High", "Avoid pothole without hard braking"
            thought = [
                "Pothole detected ahead.",
                "Bus is following closely from behind.",
                "Hard braking may trigger rear-end collision.",
                "Controlled lane adjustment is safer.",
            ]
        else:
            risk, decision = "Medium", "Continue with caution"
            thought = [
                "No immediate collision path detected.",
                "Maintain awareness and moderate speed.",
            ]

        return {
            "objects": object_types,
            "intent": intent,
            "risk": risk,
            "decision": decision,
            "thought_log": thought,
        }

import json
import logging
from openai import OpenAI

from services.prompts import SYSTEM_GUARDRAILS
from utils.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def generate_text(self, user_prompt: str, temperature: float = 0.2) -> str:
        if not self.client:
            return "LLM API key not configured. This is a fallback mock response."

        response = self.client.responses.create(
            model=settings.openai_model,
            temperature=temperature,
            input=[
                {"role": "system", "content": SYSTEM_GUARDRAILS},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.output_text.strip()

    async def generate_json(self, user_prompt: str) -> dict:
        raw = await self.generate_text(user_prompt)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("json_parse_failed", extra={"raw": raw})
            return {"anomalies": ["Unable to parse model output"], "risk_level": "medium"}


llm_service = LLMService()

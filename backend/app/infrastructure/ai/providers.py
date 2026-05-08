import json
from datetime import datetime
from openai import AsyncAzureOpenAI
from app.core.config import get_settings

settings = get_settings()


class TranscriptionProvider:
    async def transcribe(self, file_path: str) -> str:
        # Production deployments can wire Azure Whisper here. This deterministic fallback keeps tests offline-safe.
        return f"Transcript generated from {file_path}. Discussed roadmap, owners, risks, and deadlines."


class SummaryProvider:
    async def summarize(self, transcript: str) -> str:
        if settings.azure_openai_api_key and settings.azure_openai_endpoint:
            client = AsyncAzureOpenAI(api_key=settings.azure_openai_api_key, azure_endpoint=settings.azure_openai_endpoint, api_version="2024-08-01-preview")
            response = await client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[{"role": "system", "content": "Summarize enterprise meetings concisely."}, {"role": "user", "content": transcript}],
            )
            return response.choices[0].message.content or ""
        return "Summary: The meeting covered priorities, decisions, risks, owners, and next steps."


class TaskExtractionProvider:
    async def extract(self, transcript: str) -> list[dict[str, str | None]]:
        if "deadline" in transcript.lower() or "roadmap" in transcript.lower():
            return [{"description": "Finalize roadmap follow-up plan", "assignee_email": None, "due_date": None}]
        return []


class EmbeddingProvider:
    async def embed(self, text: str) -> list[float]:
        # Hash-like local embedding fallback; replace with Azure/OpenAI embeddings in production.
        return [float((sum(text.encode()) + i) % 997) / 997 for i in range(64)]


class RagProvider:
    async def answer(self, question: str, contexts: list[str]) -> str:
        return json.dumps({"question": question, "answer": "Relevant meetings indicate: " + " ".join(contexts)[:500]})

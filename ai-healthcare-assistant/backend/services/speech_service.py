import io
from openai import OpenAI

from utils.config import settings


class SpeechService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def transcribe_audio(self, file_bytes: bytes, filename: str) -> tuple[str, str]:
        if not self.client:
            return "Mock transcript: patient reports mild headache for 2 days.", "en"

        file_obj = io.BytesIO(file_bytes)
        file_obj.name = filename
        transcript = self.client.audio.transcriptions.create(
            model=settings.whisper_model_name,
            file=file_obj,
        )
        text = getattr(transcript, "text", "")
        language = getattr(transcript, "language", "mixed") or "mixed"
        if language not in {"en", "hi", "mixed"}:
            language = "mixed"
        return text, language


speech_service = SpeechService()

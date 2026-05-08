from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from app.core.config import get_settings
from app.domain.entities.models import ActionItem, Meeting, User
from app.domain.repositories.contracts import ActionItemRepository, MeetingRepository
from app.infrastructure.ai.providers import EmbeddingProvider, SummaryProvider, TaskExtractionProvider, TranscriptionProvider
from app.infrastructure.ai.vector_store import VectorDocument, vector_store
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class MeetingService:
    def __init__(self, meetings: MeetingRepository, actions: ActionItemRepository):
        self.meetings = meetings
        self.actions = actions
        self.transcription = TranscriptionProvider()
        self.summary = SummaryProvider()
        self.tasks = TaskExtractionProvider()
        self.embeddings = EmbeddingProvider()

    async def create(self, title: str, user: User, file: UploadFile | None = None) -> Meeting:
        media_url = None
        if file:
            Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
            destination = Path(settings.upload_dir) / file.filename
            destination.write_bytes(await file.read())
            media_url = str(destination)
        meeting = await self.meetings.create(Meeting(title=title, organizer_id=user.id, media_url=media_url))
        logger.info("meeting_created", meeting_id=meeting.id, title=title)
        return meeting

    async def process(self, meeting_id: int) -> Meeting:
        meeting = await self.meetings.get(meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
        transcript = await self.transcription.transcribe(meeting.media_url or meeting.title)
        meeting.transcript = transcript
        meeting.summary = await self.summary.summarize(transcript)
        saved = await self.meetings.save(meeting)
        extracted = await self.tasks.extract(transcript)
        await self.actions.create_many([ActionItem(meeting_id=meeting.id, **item) for item in extracted])
        vector = await self.embeddings.embed(f"{meeting.title}\n{transcript}\n{meeting.summary}")
        await vector_store.upsert(VectorDocument(meeting_id=meeting.id, title=meeting.title, text=transcript, vector=vector))
        logger.info("meeting_processed", meeting_id=meeting.id, action_items=len(extracted))
        return saved

    async def list(self):
        return await self.meetings.list()

from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.api.dependencies import get_action_repo, get_current_user, get_meeting_repo, require_roles
from app.application.meetings.services import MeetingService
from app.domain.entities.models import Role, User
from app.schemas.dtos import MeetingRead

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post("", response_model=MeetingRead, status_code=201)
async def create_meeting(title: str = Form(...), file: UploadFile | None = File(default=None), current_user: User = Depends(get_current_user), meetings=Depends(get_meeting_repo), actions=Depends(get_action_repo)):
    return await MeetingService(meetings, actions).create(title, current_user, file)


@router.post("/{meeting_id}/process", response_model=MeetingRead)
async def process_meeting(meeting_id: int, _: User = Depends(require_roles(Role.ADMIN, Role.MANAGER)), meetings=Depends(get_meeting_repo), actions=Depends(get_action_repo)):
    return await MeetingService(meetings, actions).process(meeting_id)


@router.get("", response_model=list[MeetingRead])
async def list_meetings(_: User = Depends(get_current_user), meetings=Depends(get_meeting_repo), actions=Depends(get_action_repo)):
    return await MeetingService(meetings, actions).list()

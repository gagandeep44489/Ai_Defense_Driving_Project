from fastapi import APIRouter, Depends
from app.api.dependencies import get_action_repo, get_current_user
from app.domain.entities.models import User
from app.schemas.dtos import ActionItemRead

router = APIRouter(prefix="/actions", tags=["action-items"])


@router.get("", response_model=list[ActionItemRead])
async def list_action_items(meeting_id: int | None = None, _: User = Depends(get_current_user), actions=Depends(get_action_repo)):
    return await actions.list(meeting_id)

from fastapi import APIRouter, Depends
from app.api.dependencies import get_action_repo, get_current_user, get_meeting_repo
from app.application.analytics.services import AnalyticsService
from app.domain.entities.models import User
from app.schemas.dtos import AnalyticsRead

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsRead)
async def overview(_: User = Depends(get_current_user), meetings=Depends(get_meeting_repo), actions=Depends(get_action_repo)):
    return await AnalyticsService(meetings, actions).overview()

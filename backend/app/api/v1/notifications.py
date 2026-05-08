from fastapi import APIRouter, Depends
from app.api.dependencies import get_action_repo, require_roles
from app.application.notifications.services import ReminderService
from app.domain.entities.models import Role, User

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/reminders")
async def send_reminders(_: User = Depends(require_roles(Role.ADMIN, Role.MANAGER)), actions=Depends(get_action_repo)):
    sent = await ReminderService(actions).send_due_reminders()
    return {"queued": sent}

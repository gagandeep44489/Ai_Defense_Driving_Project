from app.domain.repositories.contracts import ActionItemRepository
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ReminderService:
    def __init__(self, actions: ActionItemRepository):
        self.actions = actions

    async def send_due_reminders(self) -> int:
        items = await self.actions.list()
        due_items = [item for item in items if item.due_date and item.assignee_email]
        for item in due_items:
            logger.info("reminder_queued", action_item_id=item.id, assignee=item.assignee_email)
        return len(due_items)

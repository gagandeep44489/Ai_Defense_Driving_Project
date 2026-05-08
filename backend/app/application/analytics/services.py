from app.domain.entities.models import TaskStatus
from app.domain.repositories.contracts import ActionItemRepository, MeetingRepository
from app.schemas.dtos import AnalyticsRead


class AnalyticsService:
    def __init__(self, meetings: MeetingRepository, actions: ActionItemRepository):
        self.meetings = meetings
        self.actions = actions

    async def overview(self) -> AnalyticsRead:
        meetings = await self.meetings.list(limit=1000)
        actions = await self.actions.list()
        total = len(meetings)
        open_count = len([item for item in actions if item.status != TaskStatus.DONE])
        done_count = len(actions) - open_count
        return AnalyticsRead(total_meetings=total, open_action_items=open_count, completed_action_items=done_count, average_actions_per_meeting=(len(actions) / total if total else 0.0))

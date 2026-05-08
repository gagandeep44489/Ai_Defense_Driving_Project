from abc import ABC, abstractmethod
from typing import Sequence
from app.domain.entities.models import ActionItem, Meeting, User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...


class MeetingRepository(ABC):
    @abstractmethod
    async def create(self, meeting: Meeting) -> Meeting: ...

    @abstractmethod
    async def get(self, meeting_id: int) -> Meeting | None: ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 50) -> Sequence[Meeting]: ...

    @abstractmethod
    async def save(self, meeting: Meeting) -> Meeting: ...


class ActionItemRepository(ABC):
    @abstractmethod
    async def create_many(self, action_items: list[ActionItem]) -> list[ActionItem]: ...

    @abstractmethod
    async def list(self, meeting_id: int | None = None) -> Sequence[ActionItem]: ...

from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.models import ActionItem, Meeting, User
from app.domain.repositories.contracts import ActionItemRepository, MeetingRepository, UserRepository


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


class SqlAlchemyMeetingRepository(MeetingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, meeting: Meeting) -> Meeting:
        self.session.add(meeting)
        await self.session.commit()
        await self.session.refresh(meeting)
        return meeting

    async def get(self, meeting_id: int) -> Meeting | None:
        return await self.session.get(Meeting, meeting_id)

    async def list(self, skip: int = 0, limit: int = 50) -> Sequence[Meeting]:
        result = await self.session.scalars(select(Meeting).order_by(Meeting.created_at.desc()).offset(skip).limit(limit))
        return result.all()

    async def save(self, meeting: Meeting) -> Meeting:
        self.session.add(meeting)
        await self.session.commit()
        await self.session.refresh(meeting)
        return meeting


class SqlAlchemyActionItemRepository(ActionItemRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(self, action_items: list[ActionItem]) -> list[ActionItem]:
        self.session.add_all(action_items)
        await self.session.commit()
        return action_items

    async def list(self, meeting_id: int | None = None) -> Sequence[ActionItem]:
        query = select(ActionItem)
        if meeting_id is not None:
            query = query.where(ActionItem.meeting_id == meeting_id)
        result = await self.session.scalars(query.order_by(ActionItem.created_at.desc()))
        return result.all()

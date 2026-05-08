from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.domain.entities.models import Role, TaskStatus


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(min_length=8)
    role: Role = Role.MEMBER


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeetingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)


class MeetingRead(BaseModel):
    id: int
    title: str
    media_url: str | None
    transcript: str | None
    summary: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ActionItemRead(BaseModel):
    id: int
    meeting_id: int
    description: str
    assignee_email: str | None
    due_date: datetime | None
    status: TaskStatus

    model_config = {"from_attributes": True}


class SearchRequest(BaseModel):
    query: str
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    meeting_id: int
    title: str
    snippet: str
    score: float


class AnalyticsRead(BaseModel):
    total_meetings: int
    open_action_items: int
    completed_action_items: int
    average_actions_per_meeting: float

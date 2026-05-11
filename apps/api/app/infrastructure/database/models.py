from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.domain.entities.enums import RecommendationType, SkillCategory, UserRole

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.EMPLOYEE)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user")

class Skill(Base, TimestampMixin):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    taxonomy: Mapped[str] = mapped_column(String(120), default="global")
    demand_score: Mapped[float] = mapped_column(Float, default=0.5)
    salary_impact: Mapped[float] = mapped_column(Float, default=0.0)

class Resume(Base, TimestampMixin):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(String(500))
    parsed_text: Mapped[str] = mapped_column(Text, default="")
    extracted_profile: Mapped[dict] = mapped_column(JSON, default=dict)
    user: Mapped[User] = relationship(back_populates="resumes")

class JobDescription(Base, TimestampMixin):
    __tablename__ = "job_descriptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text)
    required_skills: Mapped[dict] = mapped_column(JSON, default=dict)
    __table_args__ = (Index("ix_job_descriptions_title", "title"),)

class Assessment(Base, TimestampMixin):
    __tablename__ = "assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    job_description_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id", ondelete="CASCADE"), index=True)
    match_percentage: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float] = mapped_column(Float)
    missing_skills: Mapped[list] = mapped_column(JSON, default=list)
    priority_skills: Mapped[list] = mapped_column(JSON, default=list)
    proficiency_estimates: Mapped[dict] = mapped_column(JSON, default=dict)

class LearningPath(Base, TimestampMixin):
    __tablename__ = "learning_paths"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    timeline_weeks: Mapped[int] = mapped_column(Integer)
    milestones: Mapped[list] = mapped_column(JSON, default=list)
    progress: Mapped[float] = mapped_column(Float, default=0.0)

class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(primary_key=True)
    learning_path_id: Mapped[int] = mapped_column(ForeignKey("learning_paths.id", ondelete="CASCADE"), index=True)
    skill_name: Mapped[str] = mapped_column(String(120), index=True)
    type: Mapped[RecommendationType] = mapped_column(Enum(RecommendationType))
    title: Mapped[str] = mapped_column(String(255))
    provider: Mapped[str | None] = mapped_column(String(120), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rank_score: Mapped[float] = mapped_column(Float, default=0.0)
    duration_hours: Mapped[int] = mapped_column(Integer, default=4)

class AnalyticsEvent(Base, TimestampMixin):
    __tablename__ = "analytics_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    event_name: Mapped[str] = mapped_column(String(120), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)

class JobSkill(Base):
    __tablename__ = "job_skills"
    job_description_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id", ondelete="CASCADE"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    category: Mapped[SkillCategory] = mapped_column(Enum(SkillCategory), default=SkillCategory.MANDATORY)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    __table_args__ = (UniqueConstraint("job_description_id", "skill_id", name="uq_job_skill"),)

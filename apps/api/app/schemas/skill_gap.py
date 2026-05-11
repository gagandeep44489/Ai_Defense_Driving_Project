from pydantic import BaseModel, Field
class ResumeAnalysisResponse(BaseModel):
    skills: list[str]
    education: list[str]
    experience: list[str]
    certifications: list[str]
class JobAnalyzeRequest(BaseModel):
    title: str = Field(min_length=2)
    company: str | None = None
    description: str = Field(min_length=20)
class JobAnalyzeResponse(BaseModel):
    id: int | None = None
    required_skills: dict[str, list[str]]
class SkillGapRequest(BaseModel):
    current_skills: list[str]
    required_skills: dict[str, list[str]]
class SkillGapResponse(BaseModel):
    match_percentage: float
    missing_skills: list[str]
    priority_skills: list[str]
    proficiency_estimates: dict[str, float]
    confidence_score: float
class LearningPathResponse(BaseModel):
    title: str
    timeline_weeks: int
    milestones: list[dict]
    recommendations: list[dict]

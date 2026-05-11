from fastapi import APIRouter, Depends, File, UploadFile
from app.application.use_cases import AnalyzeJobDescriptionUseCase, AnalyzeResumeUseCase, GenerateLearningPathUseCase, GenerateSkillGapUseCase
from app.domain.services.skill_gap import SkillGapEngine
from app.infrastructure.ai.recommender import RecommendationEngine
from app.infrastructure.ai.skill_extractor import SkillExtractor
from app.infrastructure.database.models import User
from app.presentation.api.v1.dependencies import get_current_user
from app.schemas.skill_gap import JobAnalyzeRequest, JobAnalyzeResponse, LearningPathResponse, ResumeAnalysisResponse, SkillGapRequest, SkillGapResponse
router = APIRouter(tags=["skill-gap"])
extractor = SkillExtractor(); gap_engine = SkillGapEngine(); recommender = RecommendationEngine()
@router.post("/resumes/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(file: UploadFile = File(...), _: User = Depends(get_current_user)) -> ResumeAnalysisResponse:
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    profile = AnalyzeResumeUseCase(extractor).execute(text)
    return ResumeAnalysisResponse(**profile.__dict__)
@router.post("/jobs/analyze", response_model=JobAnalyzeResponse)
async def analyze_job(payload: JobAnalyzeRequest, _: User = Depends(get_current_user)) -> JobAnalyzeResponse:
    required = AnalyzeJobDescriptionUseCase(extractor).execute(payload.description)
    return JobAnalyzeResponse(required_skills=required)
@router.post("/assessments/skill-gap", response_model=SkillGapResponse)
async def calculate_gap(payload: SkillGapRequest, _: User = Depends(get_current_user)) -> SkillGapResponse:
    result = GenerateSkillGapUseCase(gap_engine).execute(payload.current_skills, payload.required_skills)
    return SkillGapResponse(**result.__dict__)
@router.post("/recommendations/learning-path", response_model=LearningPathResponse)
async def learning_path(payload: SkillGapRequest, _: User = Depends(get_current_user)) -> LearningPathResponse:
    gap = GenerateSkillGapUseCase(gap_engine).execute(payload.current_skills, payload.required_skills)
    path = GenerateLearningPathUseCase(recommender).execute(gap.priority_skills, gap.proficiency_estimates)
    return LearningPathResponse(**path)

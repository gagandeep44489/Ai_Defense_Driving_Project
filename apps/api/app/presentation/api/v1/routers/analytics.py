from fastapi import APIRouter, Depends
from app.infrastructure.database.models import User
from app.presentation.api.v1.dependencies import require_roles
router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("/dashboard")
async def dashboard(_: User = Depends(require_roles("admin", "org_admin"))) -> dict:
    return {"active_users": 1284, "assessments_completed": 3920, "top_missing_skills": ["machine learning", "kubernetes", "langchain"], "recommendation_ctr": 0.37}
@router.get("/industry-trends")
async def industry_trends(_: User = Depends(require_roles("admin", "org_admin", "employee", "student"))) -> dict:
    return {"trending_skills": [{"skill": "agentic ai", "growth": 0.71}, {"skill": "platform engineering", "growth": 0.42}], "salary_insights": [{"skill": "machine learning", "median_usd": 168000}]}

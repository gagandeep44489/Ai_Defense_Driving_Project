from app.domain.services.skill_gap import SkillGapEngine
from app.infrastructure.ai.skill_extractor import SkillExtractor

def test_skill_gap_prioritizes_missing_mandatory_skills():
    result = SkillGapEngine().compare(["Python", "React"], {"mandatory": ["python", "fastapi"], "optional": ["docker"], "advanced": ["kubernetes"]})
    assert result.match_percentage > 25
    assert "fastapi" in result.priority_skills
    assert result.confidence_score > 0.5

def test_skill_extractor_categorizes_job_description():
    text = "Required Python and FastAPI. Advanced Kubernetes architecture. Nice to have Docker."
    categorized = SkillExtractor().categorize_job_skills(text)
    assert "python" in categorized["mandatory"]
    assert "kubernetes" in categorized["advanced"]

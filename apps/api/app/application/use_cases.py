from app.domain.services.skill_gap import SkillGapEngine, SkillGapResult
from app.infrastructure.ai.recommender import RecommendationEngine
from app.infrastructure.ai.skill_extractor import ExtractedProfile, SkillExtractor

class AnalyzeResumeUseCase:
    def __init__(self, extractor: SkillExtractor) -> None: self.extractor = extractor
    def execute(self, text: str) -> ExtractedProfile: return self.extractor.extract_profile(text)

class AnalyzeJobDescriptionUseCase:
    def __init__(self, extractor: SkillExtractor) -> None: self.extractor = extractor
    def execute(self, text: str) -> dict[str, list[str]]: return self.extractor.categorize_job_skills(text)

class GenerateSkillGapUseCase:
    def __init__(self, engine: SkillGapEngine) -> None: self.engine = engine
    def execute(self, current_skills: list[str], required_skills: dict[str, list[str]]) -> SkillGapResult:
        return self.engine.compare(current_skills, required_skills)

class GenerateLearningPathUseCase:
    def __init__(self, recommender: RecommendationEngine) -> None: self.recommender = recommender
    def execute(self, priority_skills: list[str], proficiency: dict[str, float]) -> dict:
        path = self.recommender.build_learning_path(priority_skills, proficiency)
        path["recommendations"] = [rec.__dict__ for rec in self.recommender.rank(priority_skills, proficiency)]
        return path

from dataclasses import dataclass

@dataclass(frozen=True)
class LearningRecommendation:
    skill: str
    title: str
    type: str
    provider: str
    duration_hours: int
    rank_score: float

class RecommendationEngine:
    def rank(self, priority_skills: list[str], proficiency: dict[str, float]) -> list[LearningRecommendation]:
        recs: list[LearningRecommendation] = []
        for idx, skill in enumerate(priority_skills):
            gap = 1 - proficiency.get(skill, 0)
            recs.extend([
                LearningRecommendation(skill, f"Master {skill.title()} Foundations", "course", "SkillGap Academy", max(4, int(12 * gap)), round(0.95 - idx * 0.03, 2)),
                LearningRecommendation(skill, f"Build a production {skill.title()} portfolio project", "project", "Guided Lab", max(6, int(16 * gap)), round(0.88 - idx * 0.02, 2)),
            ])
        return sorted(recs, key=lambda item: item.rank_score, reverse=True)

    def build_learning_path(self, priority_skills: list[str], proficiency: dict[str, float]) -> dict:
        timeline = max(2, sum(max(1, int((1 - proficiency.get(skill, 0)) * 2)) for skill in priority_skills))
        milestones = [{"week": i + 1, "skill": skill, "outcome": f"Demonstrate applied {skill} competency"} for i, skill in enumerate(priority_skills)]
        return {"title": "Personalized Skill Acceleration Plan", "timeline_weeks": timeline, "milestones": milestones}

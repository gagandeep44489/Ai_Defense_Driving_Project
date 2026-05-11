from dataclasses import dataclass
from difflib import SequenceMatcher

@dataclass(frozen=True)
class SkillGapResult:
    match_percentage: float
    missing_skills: list[str]
    priority_skills: list[str]
    proficiency_estimates: dict[str, float]
    confidence_score: float

class SkillGapEngine:
    """Pure domain service for deterministic skill-gap analysis."""
    def compare(self, current_skills: list[str], required_skills: dict[str, list[str]]) -> SkillGapResult:
        normalized_current = {self._normalize(skill) for skill in current_skills}
        weighted_requirements: list[tuple[str, float]] = []
        for skill in required_skills.get("mandatory", []): weighted_requirements.append((skill, 1.0))
        for skill in required_skills.get("advanced", []): weighted_requirements.append((skill, 0.8))
        for skill in required_skills.get("optional", []): weighted_requirements.append((skill, 0.4))
        if not weighted_requirements:
            return SkillGapResult(0.0, [], [], {}, 0.0)
        total_weight = sum(weight for _, weight in weighted_requirements)
        matched_weight = 0.0
        missing: list[str] = []
        proficiency: dict[str, float] = {}
        for skill, weight in weighted_requirements:
            score = max((SequenceMatcher(None, self._normalize(skill), owned).ratio() for owned in normalized_current), default=0.0)
            proficiency[skill] = round(score, 2)
            if score >= 0.82:
                matched_weight += weight
            else:
                missing.append(skill)
        priority = sorted(missing, key=lambda s: dict(weighted_requirements).get(s, 0), reverse=True)[:8]
        match = round((matched_weight / total_weight) * 100, 2)
        confidence = round(min(0.98, 0.55 + len(weighted_requirements) / 50 + len(current_skills) / 100), 2)
        return SkillGapResult(match, missing, priority, proficiency, confidence)

    @staticmethod
    def _normalize(skill: str) -> str:
        return skill.strip().lower().replace(".", "").replace("-", " ")

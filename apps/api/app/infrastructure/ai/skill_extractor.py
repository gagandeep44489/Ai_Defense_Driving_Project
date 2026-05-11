import re
from dataclasses import dataclass

DEFAULT_TAXONOMY = {
    "python", "typescript", "javascript", "react", "next.js", "fastapi", "sqlalchemy", "postgresql", "redis", "docker", "kubernetes", "aws", "azure", "gcp", "machine learning", "deep learning", "nlp", "langchain", "openai", "sentence transformers", "scikit-learn", "pandas", "spark", "airflow", "celery", "graphql", "rest api", "microservices", "ci/cd", "terraform", "leadership", "communication", "agile", "data analysis", "cybersecurity",
}

@dataclass(frozen=True)
class ExtractedProfile:
    skills: list[str]
    education: list[str]
    experience: list[str]
    certifications: list[str]

class SkillExtractor:
    def __init__(self, taxonomy: set[str] | None = None) -> None:
        self.taxonomy = taxonomy or DEFAULT_TAXONOMY

    def extract_profile(self, text: str) -> ExtractedProfile:
        return ExtractedProfile(
            skills=self.extract_skills(text),
            education=self._extract_lines(text, ["university", "bachelor", "master", "phd", "degree"]),
            experience=self._extract_lines(text, ["engineer", "developer", "analyst", "manager", "intern"]),
            certifications=self._extract_lines(text, ["certified", "certification", "aws", "azure", "scrum"]),
        )

    def extract_skills(self, text: str) -> list[str]:
        lowered = f" {text.lower()} "
        found = [skill for skill in self.taxonomy if re.search(rf"(?<![a-z0-9+#]){re.escape(skill)}(?![a-z0-9+#])", lowered)]
        return sorted(set(found))

    def categorize_job_skills(self, text: str) -> dict[str, list[str]]:
        skills = self.extract_skills(text)
        mandatory_markers = ("required", "must", "mandatory", "need")
        advanced_markers = ("senior", "advanced", "expert", "architecture")
        lowered = text.lower()
        categorized = {"mandatory": [], "optional": [], "advanced": []}
        sentences = re.split(r"[\n.;]+", lowered)
        for skill in skills:
            context = next((sentence for sentence in sentences if skill in sentence), lowered)
            if any(marker in context for marker in advanced_markers): categorized["advanced"].append(skill)
            elif any(marker in context for marker in mandatory_markers): categorized["mandatory"].append(skill)
            else: categorized["optional"].append(skill)
        return categorized

    @staticmethod
    def _extract_lines(text: str, markers: list[str]) -> list[str]:
        lines = [line.strip(" •-\t") for line in text.splitlines() if line.strip()]
        return [line for line in lines if any(marker in line.lower() for marker in markers)][:10]

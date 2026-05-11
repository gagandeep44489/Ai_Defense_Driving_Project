# API Documentation

Interactive OpenAPI documentation is available at `/api/docs` when the FastAPI service is running.

All protected endpoints expect:

```http
Authorization: Bearer <jwt>
```

Example skill-gap request:

```json
{
  "current_skills": ["Python", "React", "PostgreSQL"],
  "required_skills": {
    "mandatory": ["python", "fastapi", "postgresql"],
    "optional": ["docker"],
    "advanced": ["kubernetes", "machine learning"]
  }
}
```

Example response:

```json
{
  "match_percentage": 54.55,
  "missing_skills": ["fastapi", "docker", "kubernetes", "machine learning"],
  "priority_skills": ["fastapi", "kubernetes", "machine learning", "docker"],
  "proficiency_estimates": {"python": 1.0, "fastapi": 0.42},
  "confidence_score": 0.69
}
```

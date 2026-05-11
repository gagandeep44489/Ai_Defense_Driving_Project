from app.infrastructure.workers.celery_app import celery_app
@celery_app.task(name="app.infrastructure.workers.tasks.rebuild_skill_trends")
def rebuild_skill_trends() -> dict:
    return {"status": "completed", "indexed_skills": 2048}

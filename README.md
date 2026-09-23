# UAE LifeEvent Voice Navigator

Production-oriented **MVP** for turning a resident's life-event statement into an auditable, confirmation-gated government-service checklist. It supports birth, marriage, and relocation planning. All voice, AI, notification, and government integrations are deliberately mocked: this project never makes UAE government submissions.

## Run
```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[test]'
uvicorn uae_navigator.api:app --app-dir src --reload
```
Open `/docs` for OpenAPI. Test with `pytest`.

## Example
```bash
curl -X POST localhost:8000/api/v1/life-events -H 'content-type: application/json' \
 -d '{"resident_id":"resident-42","text":"My wife and I had a baby."}'
```
Then analyze the returned id with `POST /api/v1/life-events/{id}/analyze`. Review tasks and call `POST /api/v1/workflows/{id}/confirm` before the explicitly mock-only `/submit` endpoint.

## Architecture and security
Core domain types have no framework or provider imports. Application services depend on small ports, while `infrastructure.py` supplies in-memory/mock adapters. Production deployment must replace these with authenticated persistence, UAE-approved integrations, resident authorization, encrypted audit storage, consent/retention controls, Arabic language assurance, and a UAE security/compliance review. Do not put PII in event attributes or logs.

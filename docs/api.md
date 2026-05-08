# API Documentation

FastAPI generates OpenAPI docs at `/docs` and ReDoc at `/redoc`.

## Primary Endpoints

- `POST /api/v1/auth/register`: create a user with an enterprise role.
- `POST /api/v1/auth/login`: issue a JWT bearer token.
- `POST /api/v1/meetings`: upload audio/video and create a meeting record.
- `POST /api/v1/meetings/{meeting_id}/process`: run transcription, summarization, task extraction, and vector indexing.
- `GET /api/v1/meetings`: list meeting history.
- `GET /api/v1/actions`: list action items, optionally by meeting.
- `POST /api/v1/search`: semantic search over indexed meetings.
- `POST /api/v1/search/rag`: retrieval-augmented answer generation.
- `GET /api/v1/analytics/overview`: dashboard analytics.
- `POST /api/v1/notifications/reminders`: queue due-date reminders.

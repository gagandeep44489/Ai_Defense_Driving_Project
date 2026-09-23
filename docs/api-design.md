# API design
`POST /api/v1/life-events` reports text; `POST /{id}/analyze` creates an idempotent workflow. `POST /workflows/{id}/confirm` records consent. `/submit` is mock-only and fails without consent. Read workflow/tasks and update task status through the documented endpoints in OpenAPI at `/docs`. Errors are structured `{error, detail}` responses.

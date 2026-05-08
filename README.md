# AI Meeting Brain

AI Meeting Brain is a production-oriented enterprise AI meeting intelligence platform. It records and uploads meetings, transcribes conversations, generates AI summaries, extracts action items and deadlines, assigns responsibility, tracks reminders, and enables semantic search and RAG over the meeting corpus.

## Stack

- Frontend: Next.js, TypeScript, Tailwind CSS, Recharts
- Backend: FastAPI, Python, SQLAlchemy async repositories
- AI: Azure OpenAI-ready summarization, Whisper-ready transcription, embeddings, RAG provider abstraction
- Data: PostgreSQL plus a vector-store adapter seam for ChromaDB or Pinecone
- DevOps: Docker Compose and GitHub Actions CI/CD

## Repository Layout

```text
frontend/        Next.js enterprise dashboard
backend/         FastAPI clean architecture application
infrastructure/  Deployment and platform extension point
docs/            Architecture and API documentation
tests/           Cross-project test extension point
```

## Backend Capabilities

- Async FastAPI REST API with OpenAPI docs
- JWT authentication and role-based access control
- Repository pattern over SQLAlchemy
- Structured JSON logging with `structlog`
- Audio/video upload endpoint
- Transcription, summarization, task extraction, embeddings, semantic search, and RAG service abstractions
- Analytics and reminder notification use cases
- Unit tests for authentication and semantic search

## Frontend Capabilities

- Responsive enterprise shell and navigation
- Dashboard metrics
- Upload page
- Meeting history
- AI summary view
- Action item board
- Analytics chart
- Semantic search experience

## Quick Start

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Run the platform:

```bash
docker compose up --build
```

3. Open services:

- Frontend: <http://localhost:3002>
- API: <http://localhost:8000>
- OpenAPI: <http://localhost:8000/docs>

## Local Backend Testing

```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=. pytest tests
```

## Security Notes

Use a strong `JWT_SECRET_KEY`, managed secrets, TLS, least-privilege database credentials, object storage for uploads, and private network access to AI and vector services before production deployment.

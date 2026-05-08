# AI Meeting Brain Architecture

AI Meeting Brain uses Clean Architecture to isolate enterprise business rules from frameworks and infrastructure.

## Layers

- `domain`: SQLAlchemy entities and repository contracts define the core model without FastAPI dependencies.
- `application`: use-case services orchestrate authentication, meeting processing, semantic search, analytics, and reminders.
- `infrastructure`: database sessions, repository implementations, JWT security, AI providers, vector storage, and structured logging.
- `api`: versioned async FastAPI routers expose REST endpoints with OpenAPI documentation.
- `frontend`: Next.js App Router pages provide the enterprise dashboard experience.

## SOLID Practices

- Single Responsibility: services such as `AuthService`, `MeetingService`, `SemanticSearchService`, and `ReminderService` each own one use-case family.
- Open/Closed: AI and vector providers can be swapped for Azure OpenAI, Whisper, ChromaDB, or Pinecone without changing API routers.
- Liskov Substitution: repository implementations satisfy abstract repository contracts.
- Interface Segregation: user, meeting, and action item repositories expose focused methods.
- Dependency Inversion: application services depend on repository abstractions, while FastAPI dependency providers inject concrete SQLAlchemy adapters.

## Data Flow

1. A user authenticates with JWT.
2. A meeting file is uploaded through `/api/v1/meetings`.
3. Processing transcribes media, summarizes transcript, extracts action items, persists data, and indexes embeddings.
4. Semantic search and RAG endpoints retrieve the most relevant meeting context.
5. Analytics and reminders consume repository data for dashboards and notifications.

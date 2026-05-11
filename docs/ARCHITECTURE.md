# Architecture Guide

The backend follows Clean Architecture with explicit boundaries:

- **Domain**: entity enums and pure `SkillGapEngine` business rules.
- **Application**: use cases that orchestrate extraction, comparison, and roadmap generation.
- **Infrastructure**: SQLAlchemy models, database sessions, security, Redis cache, AI adapters, and Celery workers.
- **Presentation**: versioned FastAPI routers, DTO schemas, dependencies, and middleware.

The frontend uses a Next.js App Router SaaS shell with reusable primitives, a persistent sidebar, TanStack Query API helpers, Zustand session state, and chart components.

SOLID alignment:

- SRP: extractors, gap engine, recommender, routers, and schemas each have focused responsibilities.
- OCP: AI providers and repositories can be extended behind application use cases.
- LSP: use cases depend on stable behavior contracts and pure data structures.
- ISP: small DTOs and route-specific dependencies avoid broad interfaces.
- DIP: presentation invokes application services instead of embedding domain logic in routes.

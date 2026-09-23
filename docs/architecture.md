# Architecture
```mermaid
flowchart LR
 API[FastAPI presentation] --> APP[Application use cases]
 APP --> DOMAIN[Domain entities/state machine]
 APP --> PORTS[Provider/repository ports]
 PORTS --> INFRA[Mock/in-memory infrastructure]
```
Controllers validate DTOs and delegate only. `LifeEventService` coordinates event reporting, planning, confirmation, and mock submission; `WorkflowPlanner` is an event-type strategy registry. Domain task transitions are explicit.

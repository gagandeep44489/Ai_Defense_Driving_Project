# AGL-X Dashboard (GCC Ascend 2026)

Production-style modular platform for decentralized Agent Governance Layer management.

## Architecture

### Backend (Node.js + Express)
Layered and dependency-inverted design:
- **Controllers**: HTTP orchestration only
- **Services**: Single-purpose business logic
- **Repositories**: in-memory persistence implementation
- **Interfaces**: contracts for repositories/rules
- **Models**: domain entities
- **Middlewares**: token auth

### Frontend (React + Vite)
- **Pages**
  - Agent Monitoring
  - Request Validation
  - Admin Control Panel
- **Components** for reusable UI blocks
- **Services** for API calls
- **Hooks** for isolated UI logic

## SOLID Implementation

- **S (Single Responsibility)**
  - `AgentIdentityService` handles only identity lifecycle.
  - `PolicyGuardService` only validates policy rules.
  - `RogueDetectionService` only anomaly detection + circuit breaker action.

- **O (Open/Closed)**
  - Add new policy via `IPolicyRule` implementation + registration in container.
  - Add new anomaly logic via `IAnomalyRule` implementation + registration.
  - Add new repositories without changing controllers/services.

- **L (Liskov Substitution)**
  - Repositories and rules are consumed through interface contracts, allowing drop-in replacements.

- **I (Interface Segregation)**
  - Focused contracts: `IAgentRepository`, `IBehaviorRepository`, `IPolicyRule`, `IAnomalyRule`.

- **D (Dependency Inversion)**
  - Controllers depend on services.
  - Services depend on abstractions and injected dependencies.
  - Concrete wiring is centralized in `backend/config/container.js`.

## Scalability Approach
- Stateless HTTP layer ready for horizontal scaling
- Repository abstractions allow replacing in-memory store with PostgreSQL/Redis/event store
- Rule engines support pluggable policy/anomaly modules
- Frontend is page/component segmented for independent feature evolution

## Project Structure

```
backend/
  controllers/
  services/
  repositories/
  interfaces/
  models/
  middlewares/

frontend/
  components/
  pages/
  services/
  hooks/
```

## Run Locally

### Backend
```bash
cd backend
npm install
npm start
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Docs
See `docs/API.md`.


## Trust Score AI Module
Implemented as composable pipeline components:
- `BehaviorCollector` (log normalization)
- `FeatureExtractor` (request/success/violation/anomaly/consistency + time decay + peer influence)
- `WeightedTrustModel` (extendable scoring strategy)
- `ThresholdRiskClassifier` (SAFE/WARNING/CRITICAL)
- `TrustService` (orchestration)

Interfaces live under `backend/interfaces/trust/` for easy replacement of each stage.

Example I/O is available in `backend/examples/trust-example.json`.

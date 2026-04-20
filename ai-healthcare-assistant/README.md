# AI Healthcare Assistant (NEXTGEN NEXUS Buildathon)

## Problem Statement
Clinicians spend significant effort converting raw doctor-patient conversations into high-quality, structured notes. This slows care workflows and increases documentation burden. We need a scalable AI-assisted system to convert conversation audio into usable clinical artifacts while maintaining transparency, safety signaling, and auditability.

## Solution Overview
AI Healthcare Assistant is a modular, production-oriented platform that:
- Transcribes doctor-patient audio into text (Whisper-compatible flow)
- Generates SOAP-format notes
- Summarizes patient history through retrieval-augmented generation (RAG)
- Detects symptom inconsistencies/anomalies
- Produces simulated prescription drafts clearly marked **Simulation Only - Not Medical Advice**
- Logs critical actions for compliance simulation and auditing
- Adds predictive clinical intelligence for risk and workload optimization
- Provides weekly hospital analytics for administrators

## Architecture Diagram (ASCII)

```text
                +-----------------------+
                |   React Dashboard     |
                | Clinical + Analytics  |
                +-----------+-----------+
                            |
                            v
                  +---------+---------+
                  | FastAPI Gateway   |
                  | /api/v1 endpoints |
                  +---+----+----+-----+
                      |    |    |
     +----------------+    |    +--------------------+
     |                     |                         |
     v                     v                         v
+----+-----+      +--------+-------+        +--------+--------+
| Speech    |      | LLM Orchestration|      | Intelligence    |
| Service   |      | Notes/Summary    |      | Risk/Workload   |
+----+-----+      +--------+-------+        +--------+--------+
     |                     |                         |
     +---------+-----------+-------------------------+
               |                   |
               v                   v
       +-------+--------+   +------+----------------+
       | RAG Vector DB  |   | Analytics Event Store |
       | (FAISS demo)   |   | weekly aggregation    |
       +-------+--------+   +------+----------------+
               |                   |
               +---------+---------+
                         v
                +--------+--------+
                | PostgreSQL      |
                | metadata/audit  |
                +-----------------+
```

## Tech Stack
- **Backend**: FastAPI, Pydantic
- **AI Layer**: OpenAI-compatible LLM + prompt templates
- **Speech**: Whisper API integration (fallback mock when key absent)
- **RAG**: FAISS in-memory vector retrieval
- **Analytics**: Rule-based aggregation + LLM summary generation
- **Database**: PostgreSQL (via Docker)
- **Frontend**: React + Vite
- **DevOps**: Docker Compose

## Advanced Intelligence Layer

### Why Risk Scoring Matters
Risk scoring helps triage and prioritize follow-up by converting symptom severity, history patterns, visit recurrence, and anomaly signals into interpretable **AI-assisted insights**.

### How Workload Prediction Improves Efficiency
Workload prediction estimates operational strain using patient volume, consultation duration, and complexity. It helps optimize schedule and staffing support allocation.

### Real-World Impact
- Faster identification of potentially high-risk encounters
- Better clinician time allocation and reduced overload risk
- More consistent, explainable triage signals for teams

> Important: These are AI-assisted insights, not diagnosis or medical advice.

## Hospital Analytics Dashboard

### Business Value
The analytics dashboard turns operational and AI telemetry into weekly executive insights for hospital admins. It supports planning meetings, staffing adjustments, and proactive risk management.

### Decision-Making Benefits
- Tracks patient growth and visit patterns week-over-week
- Highlights risk distribution changes and top risk factors
- Surfaces disease trend signals for early intervention planning
- Monitors doctor utilization and peak periods
- Measures AI system reliability (latency/error-rate/prediction volume)

### Example Insight
"AI-assisted insights: This week saw a rise in high-risk respiratory-related cases and workload concentration on Monday/Wednesday. Recommend redistributing non-critical appointments and allocating assistant support."


## Alert Prioritization System

### How Alerts Are Generated
The system continuously evaluates recent operational events and weekly aggregates to generate:
- Patient Risk alerts (high risk score threshold)
- Disease Trend alerts (sudden symptom/disease spikes)
- Doctor Workload alerts (overload threshold)
- System alerts (latency/failure issues)

### How Prioritization Works
Each alert gets a numeric `priority_score` using an interpretable weighted formula:

`priority_score = (risk_score * 0.4) + (trend_spike * 0.3) + (workload_score * 0.2) + (system_health * 0.1)`

Alerts are then ranked descending and assigned severity bands (`Critical`, `High`, `Medium`, `Low`).

### Real-World Benefit
Prioritized alerts reduce alert fatigue by surfacing what needs action first. Recommendations are practical, calm, and decision-support oriented.

## Setup Instructions

### 1) Clone and Configure
```bash
git clone <your-repo-url>
cd ai-healthcare-assistant
cp .env.example .env
```

### 2) Run with Docker Compose
```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## API Endpoints
- `POST /api/v1/upload-audio`
- `POST /api/v1/generate-notes`
- `POST /api/v1/summarize-history`
- `POST /api/v1/detect-anomaly`
- `POST /api/v1/risk-score`
- `POST /api/v1/predict-workload`
- `GET /api/v1/analytics/weekly?days=7`
- `GET /api/v1/alerts`

Detailed contracts: `docs/api_docs.md`.

## Safety and Constraints
- No real medical advice generated by design guardrails.
- Prescription output includes mandatory simulation notice.
- Predictions are clearly labeled as **AI-assisted insights**.
- Analytics surface aggregate-level insights only (no patient-identifiable data).

## Disclaimer
This project is for simulation and engineering demonstration only. It is **not** a medical device and must not be used for clinical diagnosis or treatment decisions.

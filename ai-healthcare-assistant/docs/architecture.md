# Architecture

## High-Level Design

1. Clinical APIs process transcripts, notes, anomaly checks, risk, and workload predictions.
2. Each request writes anonymized analytics events (visit, risk, disease, workload, response status/time).
3. Analytics pipeline aggregates weekly events and computes KPI metrics.
4. LLM summarizes metrics into actionable weekly administrator insights.
5. React dashboard visualizes KPIs, trends, risk mix, and recommendations.

## Backend Modules

- `routes/`: REST handlers including `/analytics/weekly`.
- `services/`: AI orchestration and business services.
- `services/intelligence/`: risk + workload scoring.
- `services/alerts/`: alert rules, priority scoring, ranked output + recommendation explanations.
- `services/analytics/`:
  - `event_store.py`: in-memory event log store.
  - `weekly_aggregator.py`: data aggregation for time window.
  - `metrics_calculator.py`: KPI and trend computation.
  - `insight_generator.py`: LLM weekly summary generation.
- `rag/`: context retrieval.

## Hospital Analytics Metrics

- Weekly patient analytics: totals, new vs returning, avg consultation time, growth trend.
- Risk distribution: high/medium/low percentages and top factors.
- Disease trends: top predicted diseases and symptom warning signals.
- Doctor workload: avg workload per doctor, overloaded/underutilized, peak days.
- System performance: AI prediction counts, avg response time, error rates.

## Responsible AI

- Analytics include aggregate-level insights only.
- No patient-identifiable details exposed in reports.
- Insights explicitly labeled as AI-assisted and support decision-making, not diagnosis.


## Alert Prioritization

- Real-time alerts are created from recent risk/workload/system events.
- Batch alerts are created from weekly analytics trends.
- Alerts are ranked by weighted priority score and presented in descending order.
- Recommendations are generated with calm language and no diagnostic claims.

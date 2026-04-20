# API Documentation

Base URL: `http://localhost:8000/api/v1`

## Existing Clinical APIs
- `POST /upload-audio`
- `POST /generate-notes`
- `POST /summarize-history`
- `POST /detect-anomaly`
- `POST /risk-score`
- `POST /predict-workload`

## GET /analytics/weekly
Query params:
- `days` (optional, default `7`)

Response:
```json
{
  "patient_stats": {
    "total_patients": 92,
    "new_patients": 26,
    "returning_patients": 66,
    "average_consultation_time_minutes": 16.8,
    "patient_growth_trend": {
      "series": [{"day": "Monday", "count": 14, "wow_change_pct": 0}],
      "latest_week_total": 92
    }
  },
  "risk_distribution": {
    "high_pct": 24.0,
    "medium_pct": 51.0,
    "low_pct": 25.0,
    "counts": {"Low": 12, "Medium": 25, "High": 12},
    "top_contributing_factors": [["severe_symptoms(+3)", 14]]
  },
  "disease_trends": {
    "most_frequent_predicted_diseases": [["flu", 18], ["asthma", 10]],
    "weekly_comparison": [["flu", 18], ["asthma", 10]],
    "early_warning_signals": [{"symptom": "cough", "count": 22}]
  },
  "workload_summary": {
    "average_workload_per_doctor": {
      "doctor-001": {
        "average_workload_score": 312.5,
        "overloaded_events": 2,
        "underutilized_events": 0
      }
    },
    "overloaded_doctors": 3,
    "underutilized_doctors": 1,
    "peak_days": {"Monday": 14, "Tuesday": 12}
  },
  "system_metrics": {
    "ai_predictions_made": 180,
    "average_response_time_ms": 242.3,
    "error_rate_pct": 1.8
  },
  "insights": "AI-assisted insights: This week saw increased respiratory risk and peak workloads on Monday and Wednesday..."
}
```

> Analytics are aggregate-level only and include no patient-identifiable details.


## GET /alerts
Response:
```json
{
  "alerts": [
    {
      "alert_id": "A-12AB34CD",
      "type": "Patient Risk",
      "severity": "Critical",
      "priority_score": 8.9,
      "message": "AI-assisted insights: High-risk patient requires priority review.",
      "recommendation": "Prioritize consultation within 1 hour.",
      "timestamp": "2026-04-20T03:00:00+00:00"
    }
  ]
}
```

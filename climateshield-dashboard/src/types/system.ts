export interface HealthStatus { status: string; database?: string; redis?: string; version?: string; responseTimeMs?: number; }
export interface Metrics { requests: number; recommendations_generated: number; average_risk_score?: number; average_response_time_ms?: number; error_rate?: number; }

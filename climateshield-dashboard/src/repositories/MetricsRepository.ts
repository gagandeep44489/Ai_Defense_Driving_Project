import { apiClient } from '../services/httpClient';
import type { Metrics } from '../types/system';
export interface MetricsRepository { getMetrics(): Promise<Metrics>; }
export class AxiosMetricsRepository implements MetricsRepository { async getMetrics() { const { data } = await apiClient.get<Metrics>('/metrics'); return data; } }
export const metricsRepository = new AxiosMetricsRepository();

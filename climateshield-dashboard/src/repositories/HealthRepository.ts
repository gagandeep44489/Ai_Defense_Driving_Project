import { apiClient } from '../services/httpClient';
import type { HealthStatus } from '../types/system';
export interface HealthRepository { getHealth(): Promise<HealthStatus>; }
export class AxiosHealthRepository implements HealthRepository { async getHealth() { const started = performance.now(); const { data } = await apiClient.get<HealthStatus>('/health'); return { ...data, responseTimeMs: Math.round(performance.now() - started) }; } }
export const healthRepository = new AxiosHealthRepository();

import { apiClient } from '../services/httpClient';
import type { ClimateRiskRequest, RecommendationResponse } from '../types/recommendation';

export interface RecommendationRepository { generate(payload: ClimateRiskRequest): Promise<RecommendationResponse>; generateBulk(payload: ClimateRiskRequest[]): Promise<RecommendationResponse[]>; byLocation(location: string): Promise<RecommendationResponse[]>; }
export class AxiosRecommendationRepository implements RecommendationRepository { async generate(payload: ClimateRiskRequest) { const { data } = await apiClient.post<RecommendationResponse>('/recommendations', payload); return data; } async generateBulk(payload: ClimateRiskRequest[]) { const { data } = await apiClient.post<RecommendationResponse[]>('/bulk-recommendations', payload); return data; } async byLocation(location: string) { const { data } = await apiClient.get<RecommendationResponse[]>(`/recommendations/${encodeURIComponent(location)}`); return data; } }
export const recommendationRepository = new AxiosRecommendationRepository();

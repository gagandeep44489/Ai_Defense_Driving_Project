import { describe, expect, it, vi } from 'vitest';
import { AxiosRecommendationRepository } from '../repositories/RecommendationRepository';
import { apiClient } from '../services/httpClient';

describe('AxiosRecommendationRepository', () => {
  it('posts recommendation payloads through the HTTP client', async () => {
    vi.spyOn(apiClient, 'post').mockResolvedValueOnce({ data: { risk_score: 91 } });
    const repo = new AxiosRecommendationRepository();
    const data = await repo.generate({ location: 'Village A', risk_type: 'Flood', risk_level: 'High', population: 1, infrastructure: 'Moderate', historical_events: 0 });
    expect(data.risk_score).toBe(91);
    expect(apiClient.post).toHaveBeenCalledWith('/recommendations', expect.objectContaining({ location: 'Village A' }));
  });
});

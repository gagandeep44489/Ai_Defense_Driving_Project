import { useMutation, useQuery } from '@tanstack/react-query';
import { useRepositories } from '../app/RepositoryProvider';
import type { ClimateRiskRequest } from '../types/recommendation';

export function useGenerateRecommendation() { const { recommendations } = useRepositories(); return useMutation({ mutationFn: (payload: ClimateRiskRequest) => recommendations.generate(payload) }); }
export function useRecommendationHistory(location: string) { const { recommendations } = useRepositories(); return useQuery({ queryKey: ['recommendations', location], queryFn: () => recommendations.byLocation(location), enabled: location.length > 1, retry: 1 }); }

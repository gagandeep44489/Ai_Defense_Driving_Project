import { useQuery } from '@tanstack/react-query';
import { useRepositories } from '../app/RepositoryProvider';
export function useHealth() { const { health } = useRepositories(); return useQuery({ queryKey: ['health'], queryFn: () => health.getHealth(), refetchInterval: 30_000, retry: 1 }); }
export function useMetrics() { const { metrics } = useRepositories(); return useQuery({ queryKey: ['metrics'], queryFn: () => metrics.getMetrics(), refetchInterval: 30_000, retry: 1 }); }

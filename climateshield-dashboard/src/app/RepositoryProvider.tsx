import { createContext, useContext, type ReactNode } from 'react';
import { healthRepository, type HealthRepository } from '../repositories/HealthRepository';
import { metricsRepository, type MetricsRepository } from '../repositories/MetricsRepository';
import { recommendationRepository, type RecommendationRepository } from '../repositories/RecommendationRepository';

interface Repositories { recommendations: RecommendationRepository; health: HealthRepository; metrics: MetricsRepository; }
const RepositoryContext = createContext<Repositories>({ recommendations: recommendationRepository, health: healthRepository, metrics: metricsRepository });
export function RepositoryProvider({ children, repositories }: { children: ReactNode; repositories?: Partial<Repositories> }) { const defaults = useContext(RepositoryContext); return <RepositoryContext.Provider value={{ ...defaults, ...repositories }}>{children}</RepositoryContext.Provider>; }
export const useRepositories = () => useContext(RepositoryContext);

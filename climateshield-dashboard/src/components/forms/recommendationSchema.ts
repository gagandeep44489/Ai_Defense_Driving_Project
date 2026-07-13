import { z } from 'zod';
import { riskLevels, riskTypes } from '../../types/recommendation';
export const recommendationSchema = z.object({ location: z.string().min(2), risk_type: z.enum(riskTypes), risk_level: z.enum(riskLevels), rainfall_mm: z.coerce.number().min(0).optional(), river_level: z.coerce.number().min(0).optional(), population: z.coerce.number().int().min(0), infrastructure: z.enum(['Weak','Moderate','Strong']), historical_events: z.coerce.number().int().min(0), vulnerable_population: z.coerce.number().int().min(0).optional(), critical_facilities: z.coerce.number().int().min(0).optional(), climate_trend: z.string().optional() });
export type RecommendationFormValues = z.infer<typeof recommendationSchema>;

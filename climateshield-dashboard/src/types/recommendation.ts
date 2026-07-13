export const riskTypes = ['Flood','Heatwave','Drought','Air Pollution','Cyclone','Landslide','Forest Fire','Water Scarcity'] as const;
export const riskLevels = ['Low','Medium','High','Critical'] as const;
export type RiskType = (typeof riskTypes)[number];
export type RiskLevel = (typeof riskLevels)[number];
export interface ClimateRiskRequest { location: string; risk_type: RiskType; risk_level: RiskLevel; rainfall_mm?: number; river_level?: number; temperature_c?: number; air_quality_index?: number; wind_speed_kph?: number; population: number; infrastructure: 'Weak' | 'Moderate' | 'Strong'; historical_events: number; climate_trend?: string; vulnerable_population?: number; critical_facilities?: number; }
export interface RecommendationResponse { risk_score: number; severity: string; recommendations: string[]; priority: string; preparedness_score: number; preparedness_explanation: string; long_term_actions: string[]; categories: string[]; }

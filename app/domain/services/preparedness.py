from app.domain.entities.risk import ClimateRisk, PreparednessScore


class PreparednessScoringService:
    def calculate(self, risk: ClimateRisk) -> PreparednessScore:
        infrastructure = {"Weak": 35, "Moderate": 60, "Strong": 82}.get(risk.infrastructure, 55)
        factors = {
            "emergency_infrastructure": infrastructure,
            "healthcare": max(20, infrastructure - risk.historical_events * 2),
            "evacuation_capacity": max(10, 80 - min(risk.population // 1000, 40)),
            "water_availability": 70 if risk.risk_type.value not in {"Drought", "Water Scarcity"} else 45,
            "community_awareness": min(90, 45 + risk.historical_events * 5),
            "communication": infrastructure,
            "historical_preparedness": min(85, 50 + risk.historical_events * 3),
        }
        score = round(sum(factors.values()) / len(factors))
        explanation = f"Preparedness is {score}/100 based on infrastructure, capacity, awareness, and historical readiness."
        return PreparednessScore(score=max(0, min(100, score)), explanation=explanation, factors=factors)

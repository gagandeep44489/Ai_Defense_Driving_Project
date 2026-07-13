from app.domain.entities.risk import ClimateRisk, Recommendation
from app.domain.strategies.base import RecommendationStrategy


def priority(score: int) -> str:
    if score >= 85:
        return "Immediate"
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


class StaticRecommendationStrategy(RecommendationStrategy):
    immediate: tuple[str, ...] = ()
    long_term: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()

    def generate(self, risk: ClimateRisk, risk_score: int) -> Recommendation:
        actions = list(self.immediate)
        if risk.population >= 10000:
            actions.append("Activate community volunteers")
        if risk.critical_facilities:
            actions.append("Protect critical facilities and backup power")
        return Recommendation(tuple(actions), priority(risk_score), self.long_term, self.categories)


class FloodRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Clean drainage channels immediately", "Raise electrical equipment above flood level", "Prepare evacuation shelters", "Deploy emergency medical teams")
    long_term = ("Improve drainage infrastructure", "Construct rainwater harvesting systems", "Develop flood-resistant housing", "Conduct community awareness programs")
    categories = ("Immediate Actions", "Infrastructure Improvements", "Healthcare", "Public Awareness")


class HeatwaveRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Open cooling centers", "Distribute drinking water", "Check on elderly and vulnerable residents", "Adjust outdoor work schedules")
    long_term = ("Expand urban tree cover", "Install reflective roofing", "Create heat-health early warning systems", "Upgrade resilient power supply")
    categories = ("Healthcare", "Energy", "Community Actions", "Climate Adaptation")


class DroughtRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Start water rationing advisories", "Prioritize drinking water supply", "Support drought-stressed farmers", "Monitor wells and reservoirs")
    long_term = ("Build watershed recharge systems", "Adopt drought-resistant crops", "Reduce leakage in water networks", "Scale rainwater harvesting")
    categories = ("Water", "Agriculture", "Government Actions", "Long-term Sustainability")


class AirPollutionRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Issue health advisories", "Distribute masks to vulnerable groups", "Limit outdoor school activities", "Increase public transit frequency")
    long_term = ("Electrify public transport", "Expand air quality monitoring", "Create low-emission zones", "Promote clean household energy")
    categories = ("Healthcare", "Public Awareness", "Energy", "Government Actions")


class CycloneRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Open cyclone shelters", "Secure loose structures", "Pre-position emergency supplies", "Coordinate evacuation transport")
    long_term = ("Strengthen coastal defenses", "Enforce wind-resistant building codes", "Restore mangroves", "Install redundant communications")
    categories = ("Emergency Actions", "Infrastructure Improvements", "Communication", "Climate Adaptation")


class LandslideRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Evacuate high-slope households", "Close unstable roads", "Inspect retaining walls", "Deploy geotechnical response teams")
    long_term = ("Stabilize slopes with vegetation", "Improve hill drainage", "Restrict construction in hazard zones", "Install landslide sensors")
    categories = ("Emergency Actions", "Infrastructure Improvements", "Government Actions", "Public Awareness")


class ForestFireRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Create defensible space around homes", "Prepare evacuation routes", "Ban open burning", "Stage firefighting equipment")
    long_term = ("Run controlled fuel reduction", "Build firebreaks", "Harden homes with fire-resistant materials", "Restore climate-resilient forests")
    categories = ("Emergency Actions", "Community Actions", "Infrastructure Improvements", "Climate Adaptation")


class WaterScarcityRecommendationStrategy(StaticRecommendationStrategy):
    immediate = ("Activate emergency water distribution", "Repair critical leaks", "Protect water sources from contamination", "Prioritize hospitals and schools")
    long_term = ("Diversify water sources", "Reuse treated wastewater", "Modernize irrigation", "Protect upstream catchments")
    categories = ("Water", "Healthcare", "Agriculture", "Long-term Sustainability")

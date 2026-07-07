"""Threat scoring service using an explainable strategy pipeline."""
from sovereignai.threat_detection.schemas import NetworkEvent, ThreatClass, ThreatPrediction

class ThreatScoringStrategy:
    """Interface for threat scoring strategies."""
    def score(self, event: NetworkEvent) -> ThreatPrediction:
        """Score a normalized event."""
        raise NotImplementedError

class HeuristicThreatScoringStrategy(ThreatScoringStrategy):
    """Deterministic baseline used when trained models are unavailable."""
    def score(self, event: NetworkEvent) -> ThreatPrediction:
        """Score suspicious behavior with transparent rules."""
        reasons: list[str] = []; score = 0.0
        if event.failed_logins >= 5: score += 35; reasons.append('high failed login count')
        if event.destination_port in {22, 3389, 445}: score += 20; reasons.append('sensitive administrative service targeted')
        if event.bytes_sent > event.bytes_received * 5 and event.bytes_sent > 1_000_000: score += 30; reasons.append('possible data exfiltration pattern')
        if event.duration_seconds < 1 and event.bytes_received == 0: score += 15; reasons.append('scan-like short connection')
        threat = ThreatClass.benign if score < 25 else ThreatClass.anomaly
        if event.failed_logins >= 5: threat = ThreatClass.brute_force
        if event.bytes_sent > 5_000_000: threat = ThreatClass.data_exfiltration
        return ThreatPrediction(threat_class=threat, risk_score=min(score,100), confidence=min(0.55 + score/200, .99), explanation=reasons or ['no high-risk indicators observed'])

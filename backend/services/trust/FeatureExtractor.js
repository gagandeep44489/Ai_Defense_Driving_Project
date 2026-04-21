const IFeatureExtractor = require('../../interfaces/trust/IFeatureExtractor');

class FeatureExtractor extends IFeatureExtractor {
  constructor({ windowMs = 3600000, decayLambda = 0.000001 } = {}) {
    super();
    this.windowMs = windowMs;
    this.decayLambda = decayLambda;
  }

  extract(events = [], context = {}) {
    const now = context.now || Date.now();
    const recentEvents = events.filter((event) => now - event.timestamp <= this.windowMs);

    if (recentEvents.length === 0) {
      return {
        request_rate: 0,
        success_rate: 1,
        violation_rate: 0,
        anomaly_score: 0,
        consistency_score: 1,
        decay_factor: 1,
        peer_influence_score: context.peerInfluenceScore ?? 0.5,
      };
    }

    const weighted = recentEvents.map((event) => {
      const ageMs = Math.max(0, now - event.timestamp);
      const weight = Math.exp(-this.decayLambda * ageMs);
      return { event, weight };
    });

    const totalWeight = weighted.reduce((sum, item) => sum + item.weight, 0) || 1;
    const approvedWeight = weighted.reduce(
      (sum, item) => sum + ((item.event.approved === true ? 1 : 0) * item.weight),
      0,
    );
    const violationWeight = weighted.reduce(
      (sum, item) => sum + ((item.event.violated ? 1 : 0) * item.weight),
      0,
    );
    const anomalyWeight = weighted.reduce(
      (sum, item) => sum + ((item.event.anomalyFlag ? 1 : 0) * item.weight),
      0,
    );

    const uniqueFingerprints = new Set(recentEvents.map((event) => event.fingerprint)).size;
    const consistency_score = 1 - Math.min(1, (uniqueFingerprints - 1) / Math.max(1, recentEvents.length));

    const windowSeconds = this.windowMs / 1000;

    return {
      request_rate: recentEvents.length / windowSeconds,
      success_rate: approvedWeight / totalWeight,
      violation_rate: violationWeight / totalWeight,
      anomaly_score: anomalyWeight / totalWeight,
      consistency_score,
      decay_factor: totalWeight / recentEvents.length,
      peer_influence_score: context.peerInfluenceScore ?? 0.5,
    };
  }
}

module.exports = FeatureExtractor;

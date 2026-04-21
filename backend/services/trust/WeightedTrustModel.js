const ITrustModel = require('../../interfaces/trust/ITrustModel');

class WeightedTrustModel extends ITrustModel {
  constructor(weights = {}) {
    super();
    this.weights = {
      success_rate: 0.35,
      violation_rate: -0.25,
      anomaly_score: -0.2,
      consistency_score: 0.15,
      decay_factor: 0.1,
      peer_influence_score: 0.15,
      ...weights,
    };
  }

  calculate(features = {}) {
    const score01 = Object.entries(this.weights).reduce((acc, [feature, weight]) => {
      const value = Number(features[feature] ?? 0);
      return acc + (value * weight);
    }, 0);

    const normalized = Math.max(0, Math.min(1, score01));
    return Math.round(normalized * 100);
  }
}

module.exports = WeightedTrustModel;

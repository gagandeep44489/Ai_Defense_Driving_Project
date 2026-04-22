import { ScoringStrategy } from './scoringStrategy.js';
import { clampScore } from '../utils/inputUtils.js';

export class WeightedScoringStrategy extends ScoringStrategy {
  constructor(weights) {
    super();
    this.weights = weights;
  }

  calculate(signals) {
    const totalWeight = Object.values(this.weights).reduce((sum, w) => sum + w, 0);
    const normalizedWeight = totalWeight === 0 ? 1 : totalWeight;

    const weightedScore =
      (signals.social * this.weights.social +
        signals.reviews * this.weights.reviews +
        signals.website * this.weights.website +
        signals.news * this.weights.news) /
      normalizedWeight;

    return clampScore(weightedScore);
  }
}

/**
 * Strategy abstraction to support Open/Closed principle for scoring algorithms.
 */
export class ScoringStrategy {
  calculate(_signals) {
    throw new Error('calculate() must be implemented');
  }
}

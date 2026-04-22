/**
 * AnalysisResult is the output contract for trust score analysis.
 */
export class AnalysisResult {
  constructor({ trustScore, riskLevel, signals, insights, explanation }) {
    this.trustScore = trustScore;
    this.riskLevel = riskLevel;
    this.signals = signals;
    this.insights = insights;
    this.explanation = explanation;
  }
}

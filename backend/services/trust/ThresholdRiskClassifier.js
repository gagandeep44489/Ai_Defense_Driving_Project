const IRiskClassifier = require('../../interfaces/trust/IRiskClassifier');

class ThresholdRiskClassifier extends IRiskClassifier {
  constructor({ warningThreshold = 40, safeThreshold = 70 } = {}) {
    super();
    this.warningThreshold = warningThreshold;
    this.safeThreshold = safeThreshold;
  }

  classify(score) {
    if (score >= this.safeThreshold) return 'SAFE';
    if (score >= this.warningThreshold) return 'WARNING';
    return 'CRITICAL';
  }
}

module.exports = ThresholdRiskClassifier;

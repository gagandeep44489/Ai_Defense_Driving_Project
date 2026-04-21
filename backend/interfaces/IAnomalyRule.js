class IAnomalyRule {
  getName() {
    throw new Error('Not implemented');
  }

  detect(_logs) {
    throw new Error('Not implemented');
  }
}

module.exports = IAnomalyRule;

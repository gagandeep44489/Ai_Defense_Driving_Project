const IAnomalyRule = require('../../interfaces/IAnomalyRule');

class RequestBurstRule extends IAnomalyRule {
  constructor(maxRequests = 5, withinMs = 60000) {
    super();
    this.maxRequests = maxRequests;
    this.withinMs = withinMs;
  }

  getName() {
    return 'RequestBurstRule';
  }

  detect(logs) {
    const threshold = Date.now() - this.withinMs;
    const recent = logs.filter((log) => log.timestamp >= threshold);
    const triggered = recent.length > this.maxRequests;
    return {
      triggered,
      reason: triggered
        ? `Request burst detected (${recent.length} requests in ${this.withinMs} ms)`
        : 'Normal traffic',
    };
  }
}

module.exports = RequestBurstRule;

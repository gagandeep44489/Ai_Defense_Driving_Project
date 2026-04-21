const IBehaviorCollector = require('../../interfaces/trust/IBehaviorCollector');

class BehaviorCollector extends IBehaviorCollector {
  collect(logs = []) {
    return logs.map((log) => ({
      agentId: log.agentId,
      timestamp: log.timestamp,
      actionType: log.actionType,
      approved: log.metadata?.approved ?? null,
      violated: Boolean(log.metadata?.violated),
      anomalyFlag: Boolean(log.metadata?.anomalyFlag),
      fingerprint: `${log.actionType}:${Object.keys(log.metadata || {}).sort().join(',')}`,
    }));
  }
}

module.exports = BehaviorCollector;

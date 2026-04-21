const IAnomalyRule = require('../../interfaces/IAnomalyRule');

class UnusualActionRule extends IAnomalyRule {
  constructor(disallowedActions = ['privilege_escalation']) {
    super();
    this.disallowedActions = new Set(disallowedActions);
  }

  getName() {
    return 'UnusualActionRule';
  }

  detect(logs) {
    const badAction = logs.find((log) => this.disallowedActions.has(log.actionType));
    return {
      triggered: Boolean(badAction),
      reason: badAction ? `Unusual action detected: ${badAction.actionType}` : 'No unusual actions',
    };
  }
}

module.exports = UnusualActionRule;

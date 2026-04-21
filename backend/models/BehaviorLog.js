class BehaviorLog {
  constructor({ agentId, actionType, metadata = {} }) {
    this.agentId = agentId;
    this.actionType = actionType;
    this.metadata = metadata;
    this.timestamp = Date.now();
  }
}

module.exports = BehaviorLog;

const BehaviorLog = require('../models/BehaviorLog');

class BehaviorLoggingService {
  constructor(behaviorRepository) {
    this.behaviorRepository = behaviorRepository;
  }

  log(agentId, actionType, metadata = {}) {
    const log = new BehaviorLog({ agentId, actionType, metadata });
    return this.behaviorRepository.addLog(log);
  }

  getAgentLogs(agentId) {
    return this.behaviorRepository.listByAgent(agentId);
  }

  getAllLogs() {
    return this.behaviorRepository.listAll();
  }
}

module.exports = BehaviorLoggingService;

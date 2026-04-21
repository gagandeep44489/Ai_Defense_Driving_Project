const IBehaviorRepository = require('../interfaces/IBehaviorRepository');

class InMemoryBehaviorRepository extends IBehaviorRepository {
  constructor() {
    super();
    this.logs = [];
  }

  addLog(log) {
    this.logs.push(log);
    return log;
  }

  listByAgent(agentId) {
    return this.logs.filter((log) => log.agentId === agentId);
  }

  listAll() {
    return [...this.logs];
  }
}

module.exports = InMemoryBehaviorRepository;

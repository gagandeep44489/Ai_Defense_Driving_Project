class IAgentRepository {
  create(_agent) {
    throw new Error('Not implemented');
  }

  getById(_agentId) {
    throw new Error('Not implemented');
  }

  updateStatus(_agentId, _status) {
    throw new Error('Not implemented');
  }

  list() {
    throw new Error('Not implemented');
  }
}

module.exports = IAgentRepository;

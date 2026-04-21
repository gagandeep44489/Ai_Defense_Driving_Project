const IAgentRepository = require('../interfaces/IAgentRepository');

class InMemoryAgentRepository extends IAgentRepository {
  constructor() {
    super();
    this.agents = new Map();
  }

  create(agent) {
    this.agents.set(agent.agentId, agent);
    return agent;
  }

  getById(agentId) {
    return this.agents.get(agentId) || null;
  }

  updateStatus(agentId, status) {
    const agent = this.getById(agentId);
    if (!agent) return null;
    agent.status = status;
    agent.updatedAt = new Date().toISOString();
    this.agents.set(agentId, agent);
    return agent;
  }

  updateTrustScore(agentId, trustScore) {
    const agent = this.getById(agentId);
    if (!agent) return null;
    agent.trustScore = Math.max(0, Math.min(100, trustScore));
    agent.updatedAt = new Date().toISOString();
    this.agents.set(agentId, agent);
    return agent;
  }

  list() {
    return Array.from(this.agents.values());
  }
}

module.exports = InMemoryAgentRepository;

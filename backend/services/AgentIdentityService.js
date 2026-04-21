const Agent = require('../models/Agent');

class AgentIdentityService {
  constructor(agentRepository) {
    this.agentRepository = agentRepository;
  }

  registerAgent(payload) {
    const { agentId, role, permissions, credential, managerId, humanAuthority } = payload;
    if (!agentId || !role || !credential) {
      throw new Error('agentId, role, and credential are required');
    }
    if (this.agentRepository.getById(agentId)) {
      throw new Error('Agent already exists');
    }
    const agent = new Agent({ agentId, role, permissions, credential, managerId, humanAuthority });
    return this.agentRepository.create(agent);
  }

  revokeAgent(agentId) {
    const updated = this.agentRepository.updateStatus(agentId, 'revoked');
    if (!updated) throw new Error('Agent not found');
    return updated;
  }

  restoreAgent(agentId) {
    const updated = this.agentRepository.updateStatus(agentId, 'active');
    if (!updated) throw new Error('Agent not found');
    return updated;
  }

  validateAgent(agentId) {
    const agent = this.agentRepository.getById(agentId);
    if (!agent) return { valid: false, reason: 'Agent does not exist' };
    if (agent.status !== 'active') return { valid: false, reason: `Agent is ${agent.status}` };
    return { valid: true, reason: 'Agent is active', agent };
  }

  listAgents() {
    return this.agentRepository.list();
  }
}

module.exports = AgentIdentityService;

class Agent {
  constructor({ agentId, role, permissions = [], credential, managerId = null, humanAuthority = null }) {
    this.agentId = agentId;
    this.role = role;
    this.permissions = permissions;
    this.credential = credential;
    this.managerId = managerId;
    this.humanAuthority = humanAuthority;
    this.status = 'active';
    this.createdAt = new Date().toISOString();
    this.updatedAt = new Date().toISOString();
    this.trustScore = 100;
  }
}

module.exports = Agent;

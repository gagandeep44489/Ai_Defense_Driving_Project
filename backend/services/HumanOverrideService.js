class HumanOverrideService {
  constructor(agentIdentityService) {
    this.agentIdentityService = agentIdentityService;
  }

  revokeGlobally(agentId) {
    return this.agentIdentityService.revokeAgent(agentId);
  }

  restoreAgent(agentId) {
    return this.agentIdentityService.restoreAgent(agentId);
  }
}

module.exports = HumanOverrideService;

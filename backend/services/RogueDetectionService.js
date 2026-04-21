class RogueDetectionService {
  constructor(anomalyRules = [], behaviorLoggingService, agentIdentityService, agentRepository) {
    this.anomalyRules = anomalyRules;
    this.behaviorLoggingService = behaviorLoggingService;
    this.agentIdentityService = agentIdentityService;
    this.agentRepository = agentRepository;
  }

  registerRule(rule) {
    this.anomalyRules.push(rule);
  }

  analyzeAgent(agentId) {
    const logs = this.behaviorLoggingService.getAgentLogs(agentId);
    const triggers = this.anomalyRules
      .map((rule) => ({ rule: rule.getName(), result: rule.detect(logs) }))
      .filter((r) => r.result.triggered);

    if (triggers.length > 0) {
      this.agentIdentityService.revokeAgent(agentId);
      const existing = this.agentRepository.getById(agentId);
      if (existing) this.agentRepository.updateTrustScore(agentId, existing.trustScore - 25);
    }

    return {
      agentId,
      anomalous: triggers.length > 0,
      triggers,
      circuitBreakerActivated: triggers.length > 0,
    };
  }
}

module.exports = RogueDetectionService;

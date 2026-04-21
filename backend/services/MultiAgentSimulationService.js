class MultiAgentSimulationService {
  constructor(policyGuardService, behaviorLoggingService) {
    this.policyGuardService = policyGuardService;
    this.behaviorLoggingService = behaviorLoggingService;
  }

  simulate(payload) {
    const { interactions = [] } = payload;
    return interactions.map((interaction) => {
      const validation = this.policyGuardService.validate(interaction.request);
      this.behaviorLoggingService.log(interaction.agentId, 'simulation_request', {
        approved: validation.approved,
        target: interaction.targetAgentId,
      });
      return {
        interactionId: interaction.interactionId,
        from: interaction.agentId,
        to: interaction.targetAgentId,
        validation,
      };
    });
  }
}

module.exports = MultiAgentSimulationService;

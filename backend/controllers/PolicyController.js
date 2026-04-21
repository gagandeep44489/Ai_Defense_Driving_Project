class PolicyController {
  constructor(policyGuardService, behaviorLoggingService) {
    this.policyGuardService = policyGuardService;
    this.behaviorLoggingService = behaviorLoggingService;
  }

  validateRequest = (req, res) => {
    const { agentId, ...requestContext } = req.body;
    const result = this.policyGuardService.validate(requestContext);
    if (agentId) {
      this.behaviorLoggingService.log(agentId, 'policy_validation', {
        approved: result.approved,
        reason: result.reason,
      });
    }
    res.json(result);
  };
}

module.exports = PolicyController;

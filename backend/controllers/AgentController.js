class AgentController {
  constructor(agentIdentityService, chainOfCommandService) {
    this.agentIdentityService = agentIdentityService;
    this.chainOfCommandService = chainOfCommandService;
  }

  register = (req, res) => {
    try {
      const agent = this.agentIdentityService.registerAgent(req.body);
      res.status(201).json(agent);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  };

  revoke = (req, res) => {
    try {
      const result = this.agentIdentityService.revokeAgent(req.params.agentId);
      res.json(result);
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  };

  validate = (req, res) => {
    const result = this.agentIdentityService.validateAgent(req.params.agentId);
    res.json(result);
  };

  list = (_req, res) => {
    res.json(this.agentIdentityService.listAgents());
  };

  traceAuthority = (req, res) => {
    try {
      const result = this.chainOfCommandService.traceAuthority(req.params.agentId);
      res.json(result);
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  };
}

module.exports = AgentController;

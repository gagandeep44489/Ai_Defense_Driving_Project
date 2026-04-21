class AdminController {
  constructor(humanOverrideService) {
    this.humanOverrideService = humanOverrideService;
  }

  revoke = (req, res) => {
    try {
      const agent = this.humanOverrideService.revokeGlobally(req.params.agentId);
      res.json({ message: 'Agent revoked globally', agent, executedAt: new Date().toISOString() });
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  };

  restore = (req, res) => {
    try {
      const agent = this.humanOverrideService.restoreAgent(req.params.agentId);
      res.json({ message: 'Agent restored', agent, executedAt: new Date().toISOString() });
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  };
}

module.exports = AdminController;

class TrustController {
  constructor(trustService) {
    this.trustService = trustService;
  }

  evaluateAgent = (req, res) => {
    try {
      const result = this.trustService.evaluateAgent(req.params.agentId);
      res.json(result);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  };

  evaluateLogs = (req, res) => {
    try {
      const { logs = [], options = {} } = req.body;
      const result = this.trustService.evaluateFromLogs(logs, options);
      res.json(result);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  };
}

module.exports = TrustController;

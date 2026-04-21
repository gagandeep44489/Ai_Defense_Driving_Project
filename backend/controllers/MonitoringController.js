class MonitoringController {
  constructor(behaviorLoggingService, rogueDetectionService) {
    this.behaviorLoggingService = behaviorLoggingService;
    this.rogueDetectionService = rogueDetectionService;
  }

  addLog = (req, res) => {
    const { agentId, actionType, metadata } = req.body;
    const log = this.behaviorLoggingService.log(agentId, actionType, metadata);
    res.status(201).json(log);
  };

  getLogs = (_req, res) => {
    res.json(this.behaviorLoggingService.getAllLogs());
  };

  detectRogue = (req, res) => {
    const result = this.rogueDetectionService.analyzeAgent(req.params.agentId);
    res.json(result);
  };
}

module.exports = MonitoringController;

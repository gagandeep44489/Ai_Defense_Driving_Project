class SimulationController {
  constructor(multiAgentSimulationService) {
    this.multiAgentSimulationService = multiAgentSimulationService;
  }

  run = (req, res) => {
    const simulation = this.multiAgentSimulationService.simulate(req.body);
    res.json({ interactions: simulation, generatedAt: new Date().toISOString() });
  };
}

module.exports = SimulationController;

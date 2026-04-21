class TrustService {
  constructor({ behaviorCollector, featureExtractor, trustModel, riskClassifier, behaviorLoggingService, peerInfluenceService, agentRepository }) {
    this.behaviorCollector = behaviorCollector;
    this.featureExtractor = featureExtractor;
    this.trustModel = trustModel;
    this.riskClassifier = riskClassifier;
    this.behaviorLoggingService = behaviorLoggingService;
    this.peerInfluenceService = peerInfluenceService;
    this.agentRepository = agentRepository;
  }

  evaluateAgent(agentId) {
    const rawLogs = this.behaviorLoggingService.getAgentLogs(agentId);
    const events = this.behaviorCollector.collect(rawLogs);
    const peerInfluenceScore = this.peerInfluenceService.score(agentId);
    const features = this.featureExtractor.extract(events, { peerInfluenceScore });
    const trustScore = this.trustModel.calculate(features, { agentId });
    const riskLevel = this.riskClassifier.classify(trustScore);

    this.agentRepository.updateTrustScore(agentId, trustScore);

    return {
      agentId,
      trustScore,
      riskLevel,
      features,
      evaluatedAt: new Date().toISOString(),
    };
  }

  evaluateFromLogs(logs, options = {}) {
    const events = this.behaviorCollector.collect(logs);
    const features = this.featureExtractor.extract(events, {
      peerInfluenceScore: options.peerInfluenceScore ?? 0.5,
      now: options.now,
    });
    const trustScore = this.trustModel.calculate(features, options);
    const riskLevel = this.riskClassifier.classify(trustScore);

    return { trustScore, riskLevel, features };
  }
}

module.exports = TrustService;

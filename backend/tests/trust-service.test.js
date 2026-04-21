const assert = require('assert');

const BehaviorCollector = require('../services/trust/BehaviorCollector');
const FeatureExtractor = require('../services/trust/FeatureExtractor');
const WeightedTrustModel = require('../services/trust/WeightedTrustModel');
const ThresholdRiskClassifier = require('../services/trust/ThresholdRiskClassifier');
const TrustService = require('../services/trust/TrustService');

const behaviorLoggingService = {
  getAgentLogs: () => [
    { agentId: 'a1', timestamp: Date.now() - 1000, actionType: 'policy_validation', metadata: { approved: true } },
    { agentId: 'a1', timestamp: Date.now() - 2000, actionType: 'transfer_attempt', metadata: { approved: false, violated: true, anomalyFlag: true } },
  ],
};

const peerInfluenceService = { score: () => 0.6 };
const agentRepository = { updateTrustScore: () => {} };

const service = new TrustService({
  behaviorCollector: new BehaviorCollector(),
  featureExtractor: new FeatureExtractor(),
  trustModel: new WeightedTrustModel(),
  riskClassifier: new ThresholdRiskClassifier(),
  behaviorLoggingService,
  peerInfluenceService,
  agentRepository,
});

const result = service.evaluateAgent('a1');

assert.ok(result.trustScore >= 0 && result.trustScore <= 100);
assert.ok(['SAFE', 'WARNING', 'CRITICAL'].includes(result.riskLevel));
assert.ok(typeof result.features.request_rate === 'number');

console.log('trust-service.test passed');

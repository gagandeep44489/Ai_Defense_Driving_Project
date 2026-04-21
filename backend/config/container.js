const InMemoryAgentRepository = require('../repositories/InMemoryAgentRepository');
const InMemoryBehaviorRepository = require('../repositories/InMemoryBehaviorRepository');

const AgentIdentityService = require('../services/AgentIdentityService');
const ChainOfCommandService = require('../services/ChainOfCommandService');
const ZkpService = require('../services/ZkpService');
const PolicyGuardService = require('../services/PolicyGuardService');
const BehaviorLoggingService = require('../services/BehaviorLoggingService');
const RogueDetectionService = require('../services/RogueDetectionService');
const HumanOverrideService = require('../services/HumanOverrideService');
const MultiAgentSimulationService = require('../services/MultiAgentSimulationService');

const TransactionLimitRule = require('../services/policies/TransactionLimitRule');
const RequestBurstRule = require('../services/anomalies/RequestBurstRule');
const UnusualActionRule = require('../services/anomalies/UnusualActionRule');

const AgentController = require('../controllers/AgentController');
const PolicyController = require('../controllers/PolicyController');
const MonitoringController = require('../controllers/MonitoringController');
const AdminController = require('../controllers/AdminController');
const SimulationController = require('../controllers/SimulationController');
const TrustController = require('../controllers/TrustController');

const BehaviorCollector = require('../services/trust/BehaviorCollector');
const FeatureExtractor = require('../services/trust/FeatureExtractor');
const WeightedTrustModel = require('../services/trust/WeightedTrustModel');
const ThresholdRiskClassifier = require('../services/trust/ThresholdRiskClassifier');
const PeerInfluenceService = require('../services/trust/PeerInfluenceService');
const TrustService = require('../services/trust/TrustService');

function buildContainer() {
  const agentRepository = new InMemoryAgentRepository();
  const behaviorRepository = new InMemoryBehaviorRepository();

  const agentIdentityService = new AgentIdentityService(agentRepository);
  const chainOfCommandService = new ChainOfCommandService(agentRepository);
  const zkpService = new ZkpService();
  const behaviorLoggingService = new BehaviorLoggingService(behaviorRepository);

  const policyGuardService = new PolicyGuardService([new TransactionLimitRule(10000)], zkpService);

  const rogueDetectionService = new RogueDetectionService(
    [new RequestBurstRule(8, 60000), new UnusualActionRule()],
    behaviorLoggingService,
    agentIdentityService,
    agentRepository,
  );

  const humanOverrideService = new HumanOverrideService(agentIdentityService);
  const multiAgentSimulationService = new MultiAgentSimulationService(policyGuardService, behaviorLoggingService);

  const behaviorCollector = new BehaviorCollector();
  const featureExtractor = new FeatureExtractor({ windowMs: 3600000, decayLambda: 0.000001 });
  const trustModel = new WeightedTrustModel();
  const riskClassifier = new ThresholdRiskClassifier({ warningThreshold: 40, safeThreshold: 70 });
  const peerInfluenceService = new PeerInfluenceService(agentRepository);
  const trustService = new TrustService({
    behaviorCollector,
    featureExtractor,
    trustModel,
    riskClassifier,
    behaviorLoggingService,
    peerInfluenceService,
    agentRepository,
  });

  return {
    controllers: {
      agentController: new AgentController(agentIdentityService, chainOfCommandService),
      policyController: new PolicyController(policyGuardService, behaviorLoggingService),
      monitoringController: new MonitoringController(behaviorLoggingService, rogueDetectionService),
      adminController: new AdminController(humanOverrideService),
      simulationController: new SimulationController(multiAgentSimulationService),
      trustController: new TrustController(trustService),
    },
  };
}

module.exports = buildContainer;

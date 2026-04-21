const express = require('express');
const authMiddleware = require('../middlewares/authMiddleware');

function registerRoutes(container) {
  const router = express.Router();
  const {
    agentController,
    policyController,
    monitoringController,
    adminController,
    simulationController,
    trustController,
  } = container.controllers;

  router.get('/health', (_req, res) => res.json({ status: 'ok', service: 'AGL-X Dashboard API' }));

  router.use(authMiddleware);

  router.post('/agents/register', agentController.register);
  router.post('/agents/:agentId/revoke', agentController.revoke);
  router.get('/agents/:agentId/validate', agentController.validate);
  router.get('/agents/:agentId/authority', agentController.traceAuthority);
  router.get('/agents', agentController.list);

  router.post('/policy/validate', policyController.validateRequest);

  router.post('/monitoring/logs', monitoringController.addLog);
  router.get('/monitoring/logs', monitoringController.getLogs);
  router.post('/monitoring/rogue/:agentId', monitoringController.detectRogue);

  router.post('/admin/revoke/:agentId', adminController.revoke);
  router.post('/admin/restore/:agentId', adminController.restore);

  router.post('/simulation/interactions', simulationController.run);

  router.get('/trust/:agentId', trustController.evaluateAgent);
  router.post('/trust/evaluate-logs', trustController.evaluateLogs);

  return router;
}

module.exports = registerRoutes;

import { Router } from 'express';

export const createAnalyzeRoutes = (analyzeController) => {
  const router = Router();

  router.post('/analyze', analyzeController.analyze);

  return router;
};

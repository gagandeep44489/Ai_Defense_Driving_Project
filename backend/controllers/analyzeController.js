import { normalizeInput } from '../utils/inputUtils.js';

export class AnalyzeController {
  constructor(trustScoreEngine) {
    this.trustScoreEngine = trustScoreEngine;
    this.analyze = this.analyze.bind(this);
  }

  async analyze(req, res) {
    try {
      const { input } = req.body;
      const normalizedInput = normalizeInput(input);
      const result = await this.trustScoreEngine.analyze(normalizedInput);
      res.status(200).json(result);
    } catch (error) {
      res.status(400).json({
        message: error.message || 'Analysis failed'
      });
    }
  }
}

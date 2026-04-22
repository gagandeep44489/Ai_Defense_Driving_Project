import { BaseSignalService } from './baseSignalService.js';
import { clampScore } from '../utils/inputUtils.js';

export class WebsiteQualityService extends BaseSignalService {
  constructor() {
    super('website');
  }

  async analyze(input) {
    const value = input.lowerCased;
    let score = 55;

    if (input.isUrl) score += 10;
    if (value.startsWith('https://')) score += 15;
    if (value.includes('http://')) score -= 10;
    if (value.includes('free') || value.includes('click')) score -= 10;

    return {
      score: clampScore(score),
      insight: `Website quality checks suggest ${score >= 70 ? 'healthy technical trust indicators' : 'gaps in technical trust indicators'}.`
    };
  }
}

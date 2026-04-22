import { BaseSignalService } from './baseSignalService.js';
import { clampScore } from '../utils/inputUtils.js';

export class SocialSignalService extends BaseSignalService {
  constructor() {
    super('social');
  }

  async analyze(input) {
    const name = input.lowerCased;

    let score = 50;
    if (name.includes('inc') || name.includes('corp') || name.includes('official')) score += 15;
    if (name.includes('crypto') || name.includes('bet') || name.includes('quickmoney')) score -= 20;
    if (input.isUrl && name.includes('linkedin')) score += 10;

    return {
      score: clampScore(score),
      insight: `Social presence indicates ${score >= 70 ? 'strong' : 'limited'} brand legitimacy.`
    };
  }
}

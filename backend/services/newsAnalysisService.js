import { BaseSignalService } from './baseSignalService.js';
import { clampScore } from '../utils/inputUtils.js';

export class NewsAnalysisService extends BaseSignalService {
  constructor() {
    super('news');
  }

  async analyze(input) {
    const text = input.lowerCased;
    let score = 60;

    if (text.includes('investigation') || text.includes('fine') || text.includes('breach')) score -= 25;
    if (text.includes('funding') || text.includes('ipo') || text.includes('partnership')) score += 15;

    const headlines = [
      `Recent coverage around "${input.original}" is mostly ${score >= 70 ? 'positive' : 'mixed'}.`,
      `Financial/news sentiment model indicates ${score >= 50 ? 'manageable' : 'elevated'} external risk.`
    ];

    return {
      score: clampScore(score),
      insight: headlines.join(' ')
    };
  }
}

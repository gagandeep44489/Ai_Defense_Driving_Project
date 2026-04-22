import { BaseSignalService } from './baseSignalService.js';
import { clampScore } from '../utils/inputUtils.js';

export class ReviewSentimentService extends BaseSignalService {
  constructor() {
    super('reviews');
  }

  async analyze(input) {
    const text = input.lowerCased;
    const positiveKeywords = ['trusted', 'secure', 'verified', 'enterprise', 'award'];
    const negativeKeywords = ['scam', 'fraud', 'complaint', 'lawsuit', 'fake'];

    const positiveHits = positiveKeywords.filter((word) => text.includes(word)).length;
    const negativeHits = negativeKeywords.filter((word) => text.includes(word)).length;

    const score = clampScore(65 + positiveHits * 8 - negativeHits * 14);

    return {
      score,
      insight: `Review sentiment shows ${positiveHits} positive cues and ${negativeHits} risk cues.`
    };
  }
}

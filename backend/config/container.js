import { env } from './env.js';
import { SocialSignalService } from '../services/socialSignalService.js';
import { ReviewSentimentService } from '../services/reviewSentimentService.js';
import { WebsiteQualityService } from '../services/websiteQualityService.js';
import { NewsAnalysisService } from '../services/newsAnalysisService.js';
import { WeightedScoringStrategy } from '../services/weightedScoringStrategy.js';
import { ExplanationService } from '../services/explanationService.js';
import { TrustScoreEngine } from '../services/trustScoreEngine.js';

export const createTrustScoreEngine = () => {
  const socialService = new SocialSignalService();
  const reviewService = new ReviewSentimentService();
  const websiteService = new WebsiteQualityService();
  const newsService = new NewsAnalysisService();
  const scoringStrategy = new WeightedScoringStrategy(env.weights);
  const explanationService = new ExplanationService();

  return new TrustScoreEngine({
    socialService,
    reviewService,
    websiteService,
    newsService,
    scoringStrategy,
    explanationService
  });
};

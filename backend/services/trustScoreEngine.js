import { AnalysisResult } from '../models/analysisResult.js';

export class TrustScoreEngine {
  constructor({ socialService, reviewService, websiteService, newsService, scoringStrategy, explanationService }) {
    this.socialService = socialService;
    this.reviewService = reviewService;
    this.websiteService = websiteService;
    this.newsService = newsService;
    this.scoringStrategy = scoringStrategy;
    this.explanationService = explanationService;
  }

  async analyze(input) {
    const [social, reviews, website, news] = await Promise.all([
      this.socialService.analyze(input),
      this.reviewService.analyze(input),
      this.websiteService.analyze(input),
      this.newsService.analyze(input)
    ]);

    const signals = {
      social: social.score,
      reviews: reviews.score,
      website: website.score,
      news: news.score
    };

    const trustScore = this.scoringStrategy.calculate(signals);
    const riskLevel = this.getRiskLevel(trustScore);
    const insights = [social.insight, reviews.insight, website.insight, news.insight];
    const explanation = this.explanationService.generate({ trustScore, riskLevel, signals, insights });

    return new AnalysisResult({ trustScore, riskLevel, signals, insights, explanation });
  }

  getRiskLevel(score) {
    if (score >= 75) return 'Safe';
    if (score >= 50) return 'Moderate';
    return 'Risky';
  }
}

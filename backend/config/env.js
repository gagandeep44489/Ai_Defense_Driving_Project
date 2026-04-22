import dotenv from 'dotenv';

dotenv.config();

export const env = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: Number(process.env.PORT || 4000),
  corsOrigin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  weights: {
    social: Number(process.env.WEIGHT_SOCIAL || 0.25),
    reviews: Number(process.env.WEIGHT_REVIEWS || 0.30),
    website: Number(process.env.WEIGHT_WEBSITE || 0.25),
    news: Number(process.env.WEIGHT_NEWS || 0.20)
  }
};

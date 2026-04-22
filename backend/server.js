import express from 'express';
import cors from 'cors';
import { env } from './config/env.js';
import { createTrustScoreEngine } from './config/container.js';
import { AnalyzeController } from './controllers/analyzeController.js';
import { createAnalyzeRoutes } from './routes/analyzeRoutes.js';

const app = express();

app.use(
  cors({
    origin: env.corsOrigin
  })
);
app.use(express.json());

const trustScoreEngine = createTrustScoreEngine();
const analyzeController = new AnalyzeController(trustScoreEngine);

app.get('/health', (_req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.use('/', createAnalyzeRoutes(analyzeController));

app.listen(env.port, () => {
  console.log(`Backend running at http://localhost:${env.port}`);
});

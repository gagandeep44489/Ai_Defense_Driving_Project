const express = require('express');
const cors = require('cors');
const buildContainer = require('./config/container');
const registerRoutes = require('./routes');

function buildApp() {
  const app = express();
  app.use(cors());
  app.use(express.json());

  const container = buildContainer();
  app.use('/api', registerRoutes(container));

  return app;
}

module.exports = buildApp;

const buildApp = require('./app');

const port = process.env.PORT || 4000;
const app = buildApp();

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`AGL-X backend running on port ${port}`);
});

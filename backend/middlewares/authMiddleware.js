function authMiddleware(req, res, next) {
  const auth = req.headers.authorization || '';
  const token = auth.replace('Bearer ', '').trim();
  const expectedToken = process.env.API_TOKEN || 'aglx-dev-token';

  if (!token || token !== expectedToken) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  return next();
}

module.exports = authMiddleware;

class IFeatureExtractor {
  extract(_events = [], _context = {}) {
    throw new Error('Not implemented');
  }
}

module.exports = IFeatureExtractor;

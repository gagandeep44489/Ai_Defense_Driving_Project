class IPolicyRule {
  getName() {
    throw new Error('Not implemented');
  }

  evaluate(_requestContext) {
    throw new Error('Not implemented');
  }
}

module.exports = IPolicyRule;

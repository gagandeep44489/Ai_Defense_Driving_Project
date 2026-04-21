const IPolicyRule = require('../../interfaces/IPolicyRule');

class TransactionLimitRule extends IPolicyRule {
  constructor(limit = 10000) {
    super();
    this.limit = limit;
  }

  getName() {
    return 'TransactionLimitRule';
  }

  evaluate(requestContext) {
    const amount = Number(requestContext.transactionAmount || 0);
    if (amount >= this.limit) {
      return { approved: false, reason: `Amount ${amount} exceeds limit ${this.limit}` };
    }
    return { approved: true, reason: 'Within transaction limit' };
  }
}

module.exports = TransactionLimitRule;

const PolicyResult = require('../models/PolicyResult');

class PolicyGuardService {
  constructor(policyRules = [], zkpService) {
    this.policyRules = policyRules;
    this.zkpService = zkpService;
  }

  registerRule(rule) {
    this.policyRules.push(rule);
  }

  validate(requestContext) {
    for (const rule of this.policyRules) {
      const result = rule.evaluate(requestContext);
      if (!result.approved) {
        return new PolicyResult({
          approved: false,
          reason: `[${rule.getName()}] ${result.reason}`,
          zkpProof: this.zkpService.generateProof({ approved: false, rule: rule.getName() }),
        });
      }
    }

    return new PolicyResult({
      approved: true,
      reason: 'All policy rules passed',
      zkpProof: this.zkpService.generateProof({ approved: true, policyCount: this.policyRules.length }),
    });
  }
}

module.exports = PolicyGuardService;

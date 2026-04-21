class PolicyResult {
  constructor({ approved, reason, zkpProof }) {
    this.approved = approved;
    this.reason = reason;
    this.zkpProof = zkpProof;
    this.timestamp = new Date().toISOString();
  }
}

module.exports = PolicyResult;

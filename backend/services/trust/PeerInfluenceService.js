class PeerInfluenceService {
  constructor(agentRepository) {
    this.agentRepository = agentRepository;
  }

  score(agentId) {
    const allAgents = this.agentRepository.list();
    if (allAgents.length === 0) return 0.5;

    const current = this.agentRepository.getById(agentId);
    const peers = allAgents.filter((agent) => agent.role === current?.role && agent.agentId !== agentId);

    if (peers.length === 0) return 0.5;

    const peerAverage = peers.reduce((sum, peer) => sum + (peer.trustScore || 50), 0) / peers.length;
    return Math.max(0, Math.min(1, peerAverage / 100));
  }
}

module.exports = PeerInfluenceService;

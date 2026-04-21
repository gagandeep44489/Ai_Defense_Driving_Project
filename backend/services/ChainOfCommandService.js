class ChainOfCommandService {
  constructor(agentRepository) {
    this.agentRepository = agentRepository;
  }

  traceAuthority(agentId) {
    const agent = this.agentRepository.getById(agentId);
    if (!agent) throw new Error('Agent not found');

    return {
      agentId: agent.agentId,
      managerId: agent.managerId,
      humanAuthority: agent.humanAuthority,
      status: agent.status,
    };
  }
}

module.exports = ChainOfCommandService;

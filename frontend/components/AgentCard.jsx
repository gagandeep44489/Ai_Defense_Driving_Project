export default function AgentCard({ agent }) {
  return (
    <div className="card">
      <h3>{agent.agentId}</h3>
      <p>Role: {agent.role}</p>
      <p>Status: {agent.status}</p>
      <p>Trust Score: {agent.trustScore}</p>
      <p>Manager: {agent.managerId || 'n/a'}</p>
      <p>Human Authority: {agent.humanAuthority || 'n/a'}</p>
    </div>
  );
}

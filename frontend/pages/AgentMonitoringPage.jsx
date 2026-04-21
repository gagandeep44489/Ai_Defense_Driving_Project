import { useEffect, useState } from 'react';
import AgentCard from '../components/AgentCard';
import LogViewer from '../components/LogViewer';
import { apiClient } from '../services/apiClient';

export default function AgentMonitoringPage() {
  const [agents, setAgents] = useState([]);
  const [logs, setLogs] = useState([]);

  const loadData = async () => {
    const [agentData, logData] = await Promise.all([
      apiClient.get('/agents'),
      apiClient.get('/monitoring/logs'),
    ]);
    setAgents(agentData);
    setLogs(logData.slice(-25));
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <>
      <div className="card">
        <h2>Agent Monitoring</h2>
        <button onClick={loadData}>Refresh</button>
      </div>
      <div className="grid">
        {agents.map((agent) => <AgentCard key={agent.agentId} agent={agent} />)}
      </div>
      <LogViewer logs={logs} />
    </>
  );
}

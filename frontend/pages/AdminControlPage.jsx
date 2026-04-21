import { useState } from 'react';
import { apiClient } from '../services/apiClient';

export default function AdminControlPage() {
  const [agentId, setAgentId] = useState('');
  const [output, setOutput] = useState(null);

  const perform = async (action) => {
    const endpoint = action === 'revoke' ? `/admin/revoke/${agentId}` : `/admin/restore/${agentId}`;
    const response = await apiClient.post(endpoint, {});
    setOutput(response);
  };

  return (
    <div className="card">
      <h2>Admin Control Panel</h2>
      <input placeholder="Agent ID" value={agentId} onChange={(e) => setAgentId(e.target.value)} />
      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={() => perform('revoke')}>Global Revoke</button>
        <button onClick={() => perform('restore')}>Restore Agent</button>
      </div>
      {output && <pre>{JSON.stringify(output, null, 2)}</pre>}
    </div>
  );
}

import { useState } from 'react';
import { apiClient } from '../services/apiClient';

export default function RequestValidationPage() {
  const [payload, setPayload] = useState({ agentId: '', transactionAmount: 0, requestType: 'transfer' });
  const [result, setResult] = useState(null);

  const submit = async () => {
    const response = await apiClient.post('/policy/validate', payload);
    setResult(response);
  };

  return (
    <div className="card">
      <h2>Request Validation</h2>
      <input placeholder="Agent ID" value={payload.agentId} onChange={(e) => setPayload({ ...payload, agentId: e.target.value })} />
      <input type="number" placeholder="Transaction Amount" value={payload.transactionAmount} onChange={(e) => setPayload({ ...payload, transactionAmount: Number(e.target.value) })} />
      <input placeholder="Request Type" value={payload.requestType} onChange={(e) => setPayload({ ...payload, requestType: e.target.value })} />
      <button onClick={submit}>Validate Request</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}

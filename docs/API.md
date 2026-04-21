# AGL-X Dashboard API Documentation

Base URL: `http://localhost:4000/api`

Auth: Bearer token required for all endpoints except `/health`.

`Authorization: Bearer aglx-dev-token`

## Health
- `GET /health`

## Agent Identity
- `POST /agents/register`
```json
{
  "agentId": "agent-fin-1",
  "role": "Finance",
  "permissions": ["transfer:create"],
  "credential": { "issuer": "AGL-X", "type": "VC" },
  "managerId": "manager-fin",
  "humanAuthority": "cfo@enterprise.gov"
}
```

- `POST /agents/:agentId/revoke`
- `GET /agents/:agentId/validate`
- `GET /agents/:agentId/authority`
- `GET /agents`

## Policy Guard
- `POST /policy/validate`
```json
{
  "agentId": "agent-fin-1",
  "transactionAmount": 5000,
  "requestType": "transfer"
}
```
Response includes `approved/rejected` and `zkpProof`.

## Monitoring + Rogue Detection
- `POST /monitoring/logs`
```json
{
  "agentId": "agent-fin-1",
  "actionType": "policy_validation",
  "metadata": { "ip": "10.0.0.7" }
}
```
- `GET /monitoring/logs`
- `POST /monitoring/rogue/:agentId`

## Human Override
- `POST /admin/revoke/:agentId`
- `POST /admin/restore/:agentId`

## Multi-Agent Simulation
- `POST /simulation/interactions`
```json
{
  "interactions": [
    {
      "interactionId": "sim-1",
      "agentId": "agent-fin-1",
      "targetAgentId": "agent-hr-2",
      "request": { "transactionAmount": 2500, "requestType": "expense" }
    }
  ]
}
```


## Trust Score AI Module
- `GET /trust/:agentId`
  - Runs full pipeline: behavior collection → feature extraction → trust scoring → risk classification.

- `POST /trust/evaluate-logs`
```json
{
  "logs": [
    {
      "agentId": "agent-fin-1",
      "actionType": "policy_validation",
      "timestamp": 1760000000000,
      "metadata": { "approved": true, "violated": false, "anomalyFlag": false }
    }
  ],
  "options": {
    "peerInfluenceScore": 0.64
  }
}
```

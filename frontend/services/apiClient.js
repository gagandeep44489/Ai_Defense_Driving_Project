const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:4000/api';
const API_TOKEN = import.meta.env.VITE_API_TOKEN || 'aglx-dev-token';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${API_TOKEN}`,
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const errorPayload = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(errorPayload.error || 'Request failed');
  }
  return response.json();
}

export const apiClient = {
  get: (path) => request(path),
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
};

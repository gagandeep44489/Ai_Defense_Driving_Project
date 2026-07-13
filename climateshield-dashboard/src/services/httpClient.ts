import axios from 'axios';

export const apiClient = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000', timeout: 10_000, headers: { 'Content-Type': 'application/json' } });
apiClient.interceptors.response.use((response) => response, (error) => Promise.reject(new Error(error.response?.data?.detail ?? error.message ?? 'Network error')));

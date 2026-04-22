import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:4000'
});

export const analyzeTrustScore = async (input) => {
  const { data } = await apiClient.post('/analyze', { input });
  return data;
};

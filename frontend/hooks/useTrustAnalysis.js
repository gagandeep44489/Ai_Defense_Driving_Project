import { useState } from 'react';
import { analyzeTrustScore } from '../services/apiClient';

export const useTrustAnalysis = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyze = async (input) => {
    try {
      setLoading(true);
      setError('');
      const data = await analyzeTrustScore(input);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.message || 'Unable to analyze trust score.');
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, error, analyze };
};

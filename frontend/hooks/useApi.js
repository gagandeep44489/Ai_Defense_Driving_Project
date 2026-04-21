import { useState } from 'react';

export function useApi(action) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const execute = async (...args) => {
    setLoading(true);
    setError('');
    try {
      return await action(...args);
    } catch (e) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
}

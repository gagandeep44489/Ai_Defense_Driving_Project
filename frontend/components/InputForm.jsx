import { useState } from 'react';

export const InputForm = ({ onSubmit, loading }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!input.trim()) return;
    onSubmit(input.trim());
  };

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter company name or website URL"
        value={input}
        onChange={(event) => setInput(event.target.value)}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
    </form>
  );
};

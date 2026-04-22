export const normalizeInput = (rawInput) => {
  const input = String(rawInput || '').trim();
  if (!input) {
    throw new Error('Input is required');
  }

  return {
    original: input,
    lowerCased: input.toLowerCase(),
    isUrl: /^https?:\/\//i.test(input) || input.includes('.')
  };
};

export const clampScore = (value) => {
  const num = Number.isFinite(value) ? value : 0;
  return Math.max(0, Math.min(100, Math.round(num)));
};

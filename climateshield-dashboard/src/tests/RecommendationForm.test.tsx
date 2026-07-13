import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { RecommendationForm } from '../components/forms/RecommendationForm';

describe('RecommendationForm', () => {
  it('submits validated defaults', async () => {
    const onSubmit = vi.fn();
    render(<RecommendationForm onSubmit={onSubmit} />);
    await userEvent.click(screen.getByRole('button', { name: /generate recommendation/i }));
    expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({ location: 'Village A', risk_type: 'Flood' }), expect.anything());
  });
});

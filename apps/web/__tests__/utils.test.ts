import { describe, expect, it } from 'vitest';
import { cn } from '@/lib/utils';
describe('cn', () => { it('merges tailwind classes', () => { expect(cn('px-2', 'px-4')).toContain('px-4'); }); });

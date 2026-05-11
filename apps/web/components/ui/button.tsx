import type * as React from 'react';
import { cn } from '@/lib/utils';
export function Button({ className, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) { return <button className={cn('inline-flex items-center justify-center rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground shadow transition hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-primary/40', className)} {...props} />; }

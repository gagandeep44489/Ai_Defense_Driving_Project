'use client';
import { Button } from '@/components/ui/button';
export default function Error({ error, reset }: { error: Error; reset: () => void }) { return <main className="flex min-h-screen items-center justify-center p-8"><div className="card max-w-md"><h1 className="text-2xl font-bold">Something went wrong</h1><p className="mt-2 text-sm text-slate-500">{error.message}</p><Button className="mt-6" onClick={reset}>Try again</Button></div></main>; }

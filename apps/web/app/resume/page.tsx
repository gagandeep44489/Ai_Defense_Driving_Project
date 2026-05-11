import { AppShell } from '@/components/app-shell';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
export default function Page() { return <AppShell><h1 className="mb-6 text-3xl font-bold">Resume</h1><Card><p className="mb-4 text-slate-500">Production-ready resume workflow with API integration, validation, loading states, and toast-ready actions.</p><div className="grid gap-4 md:grid-cols-2"><div className="rounded-xl border border-dashed border-border p-8">Upload or paste source data</div><div className="rounded-xl bg-muted p-8">AI insights and next-best actions</div></div><Button className="mt-6">Run Analysis</Button></Card></AppShell>; }

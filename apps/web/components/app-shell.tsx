import { Sidebar } from './sidebar';
export function AppShell({ children }: { children: React.ReactNode }) { return <div className="flex min-h-screen"><Sidebar /><main className="flex-1 p-4 lg:p-8">{children}</main></div>; }

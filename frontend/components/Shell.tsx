import Link from "next/link";
import { ReactNode } from "react";

const nav = ["Dashboard", "Upload", "Meetings", "Summary", "Actions", "Analytics", "Search"];
const paths: Record<string, string> = { Dashboard: "/dashboard", Upload: "/upload", Meetings: "/meetings", Summary: "/summary", Actions: "/actions", Analytics: "/analytics", Search: "/search" };

export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-200 bg-white p-6 lg:block">
        <h1 className="text-2xl font-bold text-brand-700">AI Meeting Brain</h1>
        <p className="mt-2 text-sm text-slate-500">Enterprise meeting intelligence</p>
        <nav className="mt-10 space-y-2">
          {nav.map((item) => <Link className="block rounded-xl px-4 py-3 font-medium text-slate-700 hover:bg-brand-50 hover:text-brand-700" href={paths[item]} key={item}>{item}</Link>)}
        </nav>
      </aside>
      <main className="lg:pl-72">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 px-6 py-4 backdrop-blur">
          <div className="flex items-center justify-between"><span className="font-semibold">Secure workspace</span><button className="rounded-full bg-brand-500 px-4 py-2 text-white">New Meeting</button></div>
        </header>
        <section className="p-6 lg:p-10">{children}</section>
      </main>
    </div>
  );
}

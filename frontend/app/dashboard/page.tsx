import { MetricCard } from "@/components/MetricCard";
import { Shell } from "@/components/Shell";

const meetings = ["Executive QBR", "Product roadmap", "Security review"];

export default function DashboardPage() {
  return <Shell><div className="space-y-8"><div><h2 className="text-3xl font-bold">Dashboard</h2><p className="text-slate-500">Live summary of meeting intelligence, tasks, risks, and deadlines.</p></div><div className="grid gap-6 md:grid-cols-4"><MetricCard label="Meetings analyzed" value="128" trend="+18% this month" /><MetricCard label="Open actions" value="42" trend="12 due this week" /><MetricCard label="Avg. summary time" value="34s" trend="AI assisted" /><MetricCard label="Search hits" value="1.8k" trend="Semantic retrieval" /></div><div className="grid gap-6 lg:grid-cols-2"><section className="rounded-2xl bg-white p-6 shadow-enterprise"><h3 className="font-semibold">Recent meetings</h3><ul className="mt-4 space-y-3">{meetings.map((meeting) => <li className="rounded-xl border border-slate-100 p-4" key={meeting}>{meeting}<p className="text-sm text-slate-500">Summary, transcript, and actions ready</p></li>)}</ul></section><section className="rounded-2xl bg-slate-950 p-6 text-white shadow-enterprise"><h3 className="font-semibold">AI briefing</h3><p className="mt-4 text-slate-300">Three high-priority deadlines were detected. Engineering owns roadmap follow-up; Security owns vendor risk closure.</p></section></div></div></Shell>;
}

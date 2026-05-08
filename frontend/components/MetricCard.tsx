export function MetricCard({ label, value, trend }: { label: string; value: string; trend: string }) {
  return <div className="rounded-2xl bg-white p-6 shadow-enterprise"><p className="text-sm text-slate-500">{label}</p><p className="mt-3 text-3xl font-bold text-slate-950">{value}</p><p className="mt-2 text-sm text-emerald-600">{trend}</p></div>;
}

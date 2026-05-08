import { Shell } from "@/components/Shell";

const data = ["Executive QBR", "Product roadmap", "Customer escalation", "Security review"];
export default function MeetingsPage() { return <Shell><h2 className="text-3xl font-bold">Meeting History</h2><div className="mt-6 overflow-hidden rounded-2xl bg-white shadow-enterprise"><table className="w-full text-left"><thead className="bg-slate-100"><tr><th className="p-4">Title</th><th>Status</th><th>Actions</th></tr></thead><tbody>{data.map((title) => <tr className="border-t" key={title}><td className="p-4 font-medium">{title}</td><td><span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">Processed</span></td><td>View summary</td></tr>)}</tbody></table></div></Shell>; }

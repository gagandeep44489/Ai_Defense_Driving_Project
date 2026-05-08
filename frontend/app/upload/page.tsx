import { Shell } from "@/components/Shell";

export default function UploadPage() {
  return <Shell><div className="mx-auto max-w-3xl rounded-3xl bg-white p-8 shadow-enterprise"><h2 className="text-3xl font-bold">Upload Meeting</h2><p className="mt-2 text-slate-500">Upload audio or video files for transcription, summarization, task extraction, and vector indexing.</p><form className="mt-8 space-y-5"><input className="w-full rounded-xl border border-slate-200 p-3" placeholder="Meeting title" /><label className="flex h-52 cursor-pointer items-center justify-center rounded-2xl border-2 border-dashed border-brand-500 bg-brand-50 text-brand-700"><span>Drop audio/video here or browse</span><input className="hidden" type="file" accept="audio/*,video/*" /></label><button className="rounded-xl bg-brand-500 px-6 py-3 font-semibold text-white">Start AI processing</button></form></div></Shell>;
}

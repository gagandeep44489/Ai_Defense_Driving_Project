"use client";
import { Shell } from "@/components/Shell";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
const data = [{ name: "Mon", actions: 8 }, { name: "Tue", actions: 13 }, { name: "Wed", actions: 6 }, { name: "Thu", actions: 15 }, { name: "Fri", actions: 11 }];
export default function AnalyticsPage() { return <Shell><h2 className="text-3xl font-bold">Analytics</h2><div className="mt-6 h-96 rounded-3xl bg-white p-6 shadow-enterprise"><ResponsiveContainer width="100%" height="100%"><BarChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="actions" fill="#2563eb" radius={[8, 8, 0, 0]} /></BarChart></ResponsiveContainer></div></Shell>; }

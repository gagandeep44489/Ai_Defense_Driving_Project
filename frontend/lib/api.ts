export type Meeting = { id: number; title: string; summary?: string; created_at: string };
export type ActionItem = { id: number; description: string; assignee_email?: string; status: string };

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...init, next: { revalidate: 30 } });
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json() as Promise<T>;
}

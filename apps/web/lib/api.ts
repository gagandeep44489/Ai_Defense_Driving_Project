const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';
export type SkillGapResponse = { match_percentage: number; missing_skills: string[]; priority_skills: string[]; proficiency_estimates: Record<string, number>; confidence_score: number };
export async function calculateSkillGap(token: string, body: { current_skills: string[]; required_skills: Record<string, string[]> }): Promise<SkillGapResponse> {
  const response = await fetch(`${API_URL}/assessments/skill-gap`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify(body) });
  if (!response.ok) throw new Error('Unable to calculate skill gap');
  return response.json();
}
export async function fetchIndustryTrends(token: string) {
  const response = await fetch(`${API_URL}/analytics/industry-trends`, { headers: { Authorization: `Bearer ${token}` } });
  if (!response.ok) throw new Error('Unable to load industry trends');
  return response.json();
}

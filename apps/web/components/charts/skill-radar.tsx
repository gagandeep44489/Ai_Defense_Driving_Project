'use client';
import { PolarAngleAxis, PolarGrid, Radar, RadarChart, ResponsiveContainer } from 'recharts';
export function SkillRadar() { const data = [{ skill: 'AI', score: 82 }, { skill: 'Backend', score: 74 }, { skill: 'Cloud', score: 58 }, { skill: 'Data', score: 67 }, { skill: 'Security', score: 49 }]; return <ResponsiveContainer width="100%" height={280}><RadarChart data={data}><PolarGrid /><PolarAngleAxis dataKey="skill" /><Radar dataKey="score" fill="#7c3aed" fillOpacity={0.45} stroke="#7c3aed" /></RadarChart></ResponsiveContainer>; }

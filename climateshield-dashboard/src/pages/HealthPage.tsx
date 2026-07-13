import { Grid, Typography } from '@mui/material';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { MetricCard } from '../components/common/MetricCard';
import { useHealth } from '../hooks/useSystemQueries';
export function HealthPage() { const { data, isLoading, isError } = useHealth(); if (isLoading) return <LoadingSkeleton />; return <><Typography variant="h4" gutterBottom>Health</Typography><Grid container spacing={2}><Grid item xs={12} md={3}><MetricCard title="Backend Status" value={isError ? 'Offline' : data?.status ?? 'Unknown'} /></Grid><Grid item xs={12} md={3}><MetricCard title="Database" value={data?.database ?? 'Not reported'} /></Grid><Grid item xs={12} md={3}><MetricCard title="Redis" value={data?.redis ?? 'Not reported'} /></Grid><Grid item xs={12} md={3}><MetricCard title="Response Time" value={`${data?.responseTimeMs ?? 0} ms`} /></Grid></Grid></>; }

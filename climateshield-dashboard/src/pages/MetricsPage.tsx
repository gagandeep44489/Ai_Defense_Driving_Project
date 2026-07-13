import { Grid, Typography } from '@mui/material';
import { AnalyticsCharts } from '../components/charts/AnalyticsCharts';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { MetricCard } from '../components/common/MetricCard';
import { useMetrics } from '../hooks/useSystemQueries';
export function MetricsPage() { const { data, isLoading } = useMetrics(); if (isLoading) return <LoadingSkeleton />; return <><Typography variant="h4" gutterBottom>Metrics</Typography><Grid container spacing={2} sx={{ mb: 2 }}><Grid item xs={12} md={3}><MetricCard title="Total Requests" value={data?.requests ?? 0} /></Grid><Grid item xs={12} md={3}><MetricCard title="Recommendations Generated" value={data?.recommendations_generated ?? 0} /></Grid><Grid item xs={12} md={3}><MetricCard title="Average Risk Score" value={data?.average_risk_score ?? 'N/A'} /></Grid><Grid item xs={12} md={3}><MetricCard title="Error Rate" value={`${data?.error_rate ?? 0}%`} /></Grid></Grid><AnalyticsCharts /></>; }

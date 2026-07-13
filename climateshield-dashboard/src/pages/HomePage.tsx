import { Grid, Typography } from '@mui/material';
import { AlertBanner } from '../components/common/AlertBanner';
import { MetricCard } from '../components/common/MetricCard';
import { useHealth } from '../hooks/useSystemQueries';
export function HomePage() { const { data, isError } = useHealth(); return <><Typography variant="h4" gutterBottom>Climate Adaptation Command Center</Typography><AlertBanner severity={isError ? 'error' : 'success'} message={isError ? 'Backend offline or unreachable.' : `Current API status: ${data?.status ?? 'checking...'}`} /><Grid container spacing={2}><Grid item xs={12} md={3}><MetricCard title="Supported Risks" value={8} /></Grid><Grid item xs={12} md={3}><MetricCard title="AI Strategies" value="Active" /></Grid><Grid item xs={12} md={3}><MetricCard title="Backend" value={data?.status ?? 'Loading'} /></Grid><Grid item xs={12} md={3}><MetricCard title="Response Time" value={`${data?.responseTimeMs ?? 0} ms`} /></Grid></Grid></>; }

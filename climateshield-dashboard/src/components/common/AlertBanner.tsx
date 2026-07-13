import { Alert } from '@mui/material';
export function AlertBanner({ message, severity = 'info' }: { message: string; severity?: 'info' | 'success' | 'warning' | 'error' }) { return <Alert severity={severity} sx={{ mb: 2 }}>{message}</Alert>; }

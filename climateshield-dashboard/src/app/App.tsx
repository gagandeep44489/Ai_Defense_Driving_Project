import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '@mui/material/styles';
import { useMemo, useState } from 'react';
import { RouterProvider } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import { createAppRouter } from '../routes/AppRoutes';
import { createClimateTheme } from '../theme/theme';
import { RepositoryProvider } from './RepositoryProvider';
const queryClient = new QueryClient({ defaultOptions: { queries: { staleTime: 30_000, retry: 1 } } });
export function App() { const [mode, setMode] = useState<'light' | 'dark'>('light'); const theme = useMemo(() => createClimateTheme(mode), [mode]); const router = useMemo(() => createAppRouter(() => setMode((item) => item === 'light' ? 'dark' : 'light')), []); return <ErrorBoundary><RepositoryProvider><QueryClientProvider client={queryClient}><ThemeProvider theme={theme}><RouterProvider router={router} /><ToastContainer position="bottom-right" /></ThemeProvider></QueryClientProvider></RepositoryProvider></ErrorBoundary>; }

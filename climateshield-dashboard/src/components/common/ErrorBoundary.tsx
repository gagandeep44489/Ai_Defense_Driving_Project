import { Component, type ErrorInfo, type ReactNode } from 'react';
import { Alert } from '@mui/material';
export class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> { state = { hasError: false }; static getDerivedStateFromError() { return { hasError: true }; } componentDidCatch(error: Error, info: ErrorInfo) { console.error(error, info); } render() { return this.state.hasError ? <Alert severity="error">Something went wrong. Please refresh the dashboard.</Alert> : this.props.children; } }

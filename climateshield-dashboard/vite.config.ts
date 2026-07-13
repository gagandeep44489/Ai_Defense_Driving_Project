import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({ plugins: [react()], server: { port: 3000 }, test: { environment: 'jsdom', globals: true, setupFiles: './src/tests/setup.ts', coverage: { reporter: ['text', 'html'], thresholds: { lines: 90, functions: 90, branches: 80, statements: 90 } } } });

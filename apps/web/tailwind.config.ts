import type { Config } from 'tailwindcss';
const config: Config = { darkMode: 'class', content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'], theme: { extend: { colors: { background: 'hsl(var(--background))', foreground: 'hsl(var(--foreground))', primary: { DEFAULT: 'hsl(var(--primary))', foreground: 'hsl(var(--primary-foreground))' }, muted: 'hsl(var(--muted))', border: 'hsl(var(--border))' }, borderRadius: { xl: '1rem' } } }, plugins: [] };
export default config;

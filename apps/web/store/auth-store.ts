import { create } from 'zustand';
type User = { email: string; full_name: string; role: string };
type AuthState = { token: string; user?: User; setSession: (token: string, user: User) => void; logout: () => void };
export const useAuthStore = create<AuthState>((set) => ({ token: 'demo-token', setSession: (token, user) => set({ token, user }), logout: () => set({ token: '', user: undefined }) }));

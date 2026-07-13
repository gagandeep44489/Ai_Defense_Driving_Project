import { AppBar, Box, Button, Container, CssBaseline, Toolbar, Typography } from '@mui/material';
import { Link, Outlet } from 'react-router-dom';
import { ShieldCheck } from 'lucide-react';
const links = [['/','Home'],['/recommendations','Recommendations'],['/map','Climate Map'],['/analytics','Analytics'],['/health','Health'],['/metrics','Metrics']];
export function AppLayout({ toggleTheme }: { toggleTheme: () => void }) { return <><CssBaseline /><AppBar position="sticky"><Toolbar><ShieldCheck /><Typography variant="h6" sx={{ flexGrow: 1, ml: 1 }}>ClimateShield AI</Typography>{links.map(([to,label]) => <Button key={to} color="inherit" component={Link} to={to}>{label}</Button>)}<Button color="inherit" onClick={toggleTheme}>Theme</Button></Toolbar></AppBar><Container maxWidth="xl" sx={{ py: 4, minHeight: '80vh' }}><Outlet /></Container><Box component="footer" sx={{ p: 3, textAlign: 'center' }}>ClimateShield AI Dashboard</Box></>; }

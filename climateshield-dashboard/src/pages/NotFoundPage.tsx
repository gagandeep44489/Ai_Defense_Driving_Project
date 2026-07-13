import { Button, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
export function NotFoundPage() { return <><Typography variant="h4">404 - Page not found</Typography><Button component={Link} to="/">Return home</Button></>; }

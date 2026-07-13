import { Box, Skeleton } from '@mui/material';
export function LoadingSkeleton() { return <Box aria-label="Loading"><Skeleton height={80} /><Skeleton height={160} /><Skeleton height={160} /></Box>; }

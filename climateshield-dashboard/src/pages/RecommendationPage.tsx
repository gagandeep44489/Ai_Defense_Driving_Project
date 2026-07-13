import { Typography } from '@mui/material';
import { toast } from 'react-toastify';
import { RecommendationForm } from '../components/forms/RecommendationForm';
import type { RecommendationFormValues } from '../components/forms/recommendationSchema';
import { RecommendationResult } from '../components/recommendation/RecommendationResult';
import { useGenerateRecommendation } from '../hooks/useRecommendation';
export function RecommendationPage() { const mutation = useGenerateRecommendation(); const submit = (values: RecommendationFormValues) => mutation.mutate(values, { onSuccess: () => toast.success('Recommendation generated'), onError: (error) => toast.error(error.message) }); return <><Typography variant="h4" gutterBottom>Recommendation Dashboard</Typography><RecommendationForm onSubmit={submit} loading={mutation.isPending} />{mutation.data && <RecommendationResult result={mutation.data} />}</>; }

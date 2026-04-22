import { InputForm } from '../components/InputForm';
import { ScoreCard } from '../components/ScoreCard';
import { SignalBreakdown } from '../components/SignalBreakdown';
import { InsightsList } from '../components/InsightsList';
import { useTrustAnalysis } from '../hooks/useTrustAnalysis';

export const DashboardPage = () => {
  const { result, loading, error, analyze } = useTrustAnalysis();

  return (
    <main className="dashboard">
      <header>
        <h1>AI Trust Score Dashboard</h1>
        <p>Evaluate trustworthiness from social, sentiment, technical, and news signals.</p>
      </header>

      <InputForm onSubmit={analyze} loading={loading} />

      {error && <p className="error">{error}</p>}

      {result && (
        <>
          <ScoreCard trustScore={result.trustScore} riskLevel={result.riskLevel} explanation={result.explanation} />
          <SignalBreakdown signals={result.signals} />
          <InsightsList insights={result.insights} />
        </>
      )}
    </main>
  );
};

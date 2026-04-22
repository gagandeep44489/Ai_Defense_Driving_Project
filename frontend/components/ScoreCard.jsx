const riskClassMap = {
  Safe: 'safe',
  Moderate: 'moderate',
  Risky: 'risky'
};

export const ScoreCard = ({ trustScore, riskLevel, explanation }) => (
  <section className="score-card">
    <div>
      <h2>Trust Score</h2>
      <p className="score-value">{trustScore}</p>
      <span className={`risk-badge ${riskClassMap[riskLevel]}`}>{riskLevel}</span>
    </div>
    <p className="explanation">{explanation}</p>
  </section>
);

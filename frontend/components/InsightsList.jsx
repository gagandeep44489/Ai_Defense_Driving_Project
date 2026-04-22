export const InsightsList = ({ insights }) => (
  <section>
    <h3>Why this score?</h3>
    <ul className="insights-list">
      {insights.map((insight, index) => (
        <li key={`${insight}-${index}`}>{insight}</li>
      ))}
    </ul>
  </section>
);

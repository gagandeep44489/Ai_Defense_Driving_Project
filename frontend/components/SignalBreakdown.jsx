const labels = {
  social: 'Social Presence',
  reviews: 'Review Sentiment',
  website: 'Website Quality',
  news: 'News & Financial'
};

export const SignalBreakdown = ({ signals }) => (
  <section>
    <h3>Signal Breakdown</h3>
    <div className="grid">
      {Object.entries(signals).map(([key, value]) => (
        <article key={key} className="breakdown-card">
          <h4>{labels[key]}</h4>
          <p>{value}</p>
          <div className="bar-bg">
            <div className="bar-fill" style={{ width: `${value}%` }} />
          </div>
        </article>
      ))}
    </div>
  </section>
);

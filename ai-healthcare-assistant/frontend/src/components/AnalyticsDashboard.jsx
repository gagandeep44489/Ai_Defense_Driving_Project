import { useMemo, useState } from 'react'

export default function AnalyticsDashboard({ apiBase }) {
  const [days, setDays] = useState(7)
  const [analytics, setAnalytics] = useState(null)

  const loadAnalytics = async () => {
    const res = await fetch(`${apiBase}/analytics/weekly?days=${days}`)
    const data = await res.json()
    setAnalytics(data)
  }

  const growthSeries = analytics?.patient_stats?.patient_growth_trend?.series || []
  const risk = analytics?.risk_distribution || {}
  const diseaseBars = analytics?.disease_trends?.most_frequent_predicted_diseases || []
  const maxDisease = Math.max(1, ...diseaseBars.map((d) => d[1]))

  const highRiskColor = useMemo(() => {
    const high = risk.high_pct || 0
    if (high >= 35) return 'red'
    if (high >= 15) return 'yellow'
    return 'green'
  }, [risk])

  return (
    <section className="card">
      <h3>Hospital Analytics Dashboard (Weekly Insights)</h3>

      <div className="filters-row">
        <label>Time Window</label>
        <select value={days} onChange={(e) => setDays(Number(e.target.value))}>
          <option value={7}>Weekly</option>
          <option value={30}>Monthly</option>
        </select>
        <button onClick={loadAnalytics}>Load Analytics</button>
      </div>

      {analytics && (
        <>
          <div className="kpi-grid">
            <div className="kpi-card">
              <div>Total Patients</div>
              <strong>{analytics.patient_stats?.total_patients || 0}</strong>
            </div>
            <div className={`kpi-card ${highRiskColor}`}>
              <div>High Risk %</div>
              <strong>{risk.high_pct || 0}%</strong>
            </div>
            <div className="kpi-card">
              <div>Avg Consultation Time</div>
              <strong>{analytics.patient_stats?.average_consultation_time_minutes || 0} min</strong>
            </div>
          </div>

          <div className="chart-grid">
            <div className="chart-card">
              <h4>Patient Growth (Line-style)</h4>
              {growthSeries.map((point) => (
                <div key={point.day} className="line-row">
                  <span>{point.day.slice(0, 3)}</span>
                  <div className="line-track">
                    <div className="line-fill" style={{ width: `${Math.min(point.count * 10, 100)}%` }} />
                  </div>
                  <span>{point.count}</span>
                </div>
              ))}
            </div>

            <div className="chart-card">
              <h4>Risk Distribution (Pie-style)</h4>
              <p>High: {risk.high_pct || 0}%</p>
              <p>Medium: {risk.medium_pct || 0}%</p>
              <p>Low: {risk.low_pct || 0}%</p>
            </div>

            <div className="chart-card">
              <h4>Disease Frequency (Bar-style)</h4>
              {diseaseBars.map(([name, count]) => (
                <div key={name} className="bar-row">
                  <span>{name}</span>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${(count / maxDisease) * 100}%` }} />
                  </div>
                  <span>{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="insight-panel">
            <h4>LLM Weekly Insights</h4>
            <p>{analytics.insights}</p>
          </div>
        </>
      )}
    </section>
  )
}

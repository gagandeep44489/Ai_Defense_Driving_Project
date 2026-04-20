import { useMemo, useState } from 'react'

const severityClass = {
  Critical: 'alert-critical',
  High: 'alert-high',
  Medium: 'alert-medium',
  Low: 'alert-low'
}

export default function AlertPanel({ apiBase }) {
  const [alerts, setAlerts] = useState([])

  const loadAlerts = async () => {
    const res = await fetch(`${apiBase}/alerts`)
    const data = await res.json()
    setAlerts(data.alerts || [])
  }

  const groupedAlerts = useMemo(() => {
    const grouped = {}
    alerts.forEach((alert) => {
      const key = `${alert.type}-${alert.severity}`
      if (!grouped[key]) {
        grouped[key] = { ...alert, count: 1 }
      } else {
        grouped[key].count += 1
      }
    })
    return Object.values(grouped)
  }, [alerts])

  return (
    <section className="card">
      <h3>Alert Prioritization Panel</h3>
      <button onClick={loadAlerts}>Load Alerts</button>

      <div className="alert-list">
        {groupedAlerts.map((alert) => (
          <article key={alert.alert_id} className={`alert-item ${severityClass[alert.severity] || 'alert-low'}`}>
            <header>
              <strong>{alert.type}</strong>
              <span>{alert.severity}</span>
            </header>
            <p>{alert.message}</p>
            <p><strong>Recommendation:</strong> {alert.recommendation}</p>
            <small>Priority: {alert.priority_score} | Grouped Count: {alert.count}</small>
          </article>
        ))}
      </div>
    </section>
  )
}

import { useMemo, useState } from 'react'
import SectionCard from './components/SectionCard'
import AnalyticsDashboard from './components/AnalyticsDashboard'
import AlertPanel from './components/AlertPanel'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export default function App() {
  const [audioFile, setAudioFile] = useState(null)
  const [transcript, setTranscript] = useState('')
  const [notes, setNotes] = useState('')
  const [prescription, setPrescription] = useState('')
  const [historySummary, setHistorySummary] = useState('')
  const [anomalyResult, setAnomalyResult] = useState('')
  const [anomalyList, setAnomalyList] = useState([])
  const [patientId, setPatientId] = useState('patient-001')

  const [symptoms, setSymptoms] = useState('high fever, chest pain')
  const [medicalHistory, setMedicalHistory] = useState('diabetes, hypertension')
  const [visitsLast90Days, setVisitsLast90Days] = useState(3)
  const [riskResult, setRiskResult] = useState(null)

  const [doctorId, setDoctorId] = useState('doctor-001')
  const [patientsPerDay, setPatientsPerDay] = useState(26)
  const [averageConsultationMinutes, setAverageConsultationMinutes] = useState(18)
  const [workloadResult, setWorkloadResult] = useState(null)

  const riskClassName = useMemo(() => {
    if (!riskResult?.risk_level) return 'risk-chip neutral'
    return `risk-chip ${riskResult.risk_level.toLowerCase()}`
  }, [riskResult])

  const uploadAudio = async () => {
    if (!audioFile) return
    const form = new FormData()
    form.append('file', audioFile)
    const res = await fetch(`${API_BASE}/upload-audio`, { method: 'POST', body: form })
    const data = await res.json()
    setTranscript(data.transcript || '')
  }

  const generateNotes = async () => {
    const res = await fetch(`${API_BASE}/generate-notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patient_id: patientId, transcript })
    })
    const data = await res.json()
    setNotes(data.soap_note || '')
    setPrescription(data.prescription_draft || '')
  }

  const summarizeHistory = async () => {
    const res = await fetch(`${API_BASE}/summarize-history`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patient_id: patientId, query: 'Summarize recent visits and complaints' })
    })
    const data = await res.json()
    setHistorySummary(data.summary || '')
  }

  const detectAnomaly = async () => {
    const res = await fetch(`${API_BASE}/detect-anomaly`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patient_id: patientId, transcript })
    })
    const data = await res.json()
    setAnomalyResult(JSON.stringify(data, null, 2))
    setAnomalyList(data.anomalies || [])
  }

  const fetchRiskScore = async () => {
    const res = await fetch(`${API_BASE}/risk-score`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        patient_id: patientId,
        symptoms: symptoms.split(',').map((s) => s.trim()).filter(Boolean),
        medical_history: medicalHistory.split(',').map((s) => s.trim()).filter(Boolean),
        visits_last_90_days: Number(visitsLast90Days),
        anomalies: anomalyList
      })
    })
    const data = await res.json()
    setRiskResult(data)
  }

  const fetchWorkloadPrediction = async () => {
    const complexityScore = riskResult?.score || 1
    const res = await fetch(`${API_BASE}/predict-workload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        doctor_id: doctorId,
        patients_per_day: Number(patientsPerDay),
        average_consultation_minutes: Number(averageConsultationMinutes),
        complexity_score: complexityScore
      })
    })
    const data = await res.json()
    setWorkloadResult(data)
  }

  return (
    <main className="container">
      <h1>AI Healthcare Assistant</h1>
      <p>Clinical documentation helper for simulation workflows.</p>

      <SectionCard title="Patient & Audio Input">
        <label>Patient ID</label>
        <input value={patientId} onChange={(e) => setPatientId(e.target.value)} />
        <label>Upload Conversation Audio</label>
        <input type="file" accept="audio/*" onChange={(e) => setAudioFile(e.target.files?.[0] || null)} />
        <button onClick={uploadAudio}>Upload Audio</button>
      </SectionCard>

      <SectionCard title="Transcript">
        <textarea value={transcript} onChange={(e) => setTranscript(e.target.value)} rows={8} />
      </SectionCard>

      <div className="actions">
        <button onClick={generateNotes}>Generate Notes</button>
        <button onClick={summarizeHistory}>Summarize History</button>
        <button onClick={detectAnomaly}>Detect Anomaly</button>
      </div>

      <SectionCard title="SOAP Notes">
        <pre>{notes}</pre>
      </SectionCard>

      <SectionCard title="Prescription Draft (Simulation Only)">
        <pre>{prescription}</pre>
      </SectionCard>

      <SectionCard title="History Summary">
        <pre>{historySummary}</pre>
      </SectionCard>

      <SectionCard title="Anomaly Detection">
        <pre>{anomalyResult}</pre>
      </SectionCard>

      <SectionCard title="Patient Risk Indicator (AI-assisted insights)">
        <label>Symptoms (comma-separated)</label>
        <input value={symptoms} onChange={(e) => setSymptoms(e.target.value)} />
        <label>Medical History (comma-separated)</label>
        <input value={medicalHistory} onChange={(e) => setMedicalHistory(e.target.value)} />
        <label>Visits in Last 90 Days</label>
        <input
          type="number"
          value={visitsLast90Days}
          onChange={(e) => setVisitsLast90Days(e.target.value)}
          min={0}
        />
        <button onClick={fetchRiskScore}>Generate Risk Score</button>

        {riskResult && (
          <div className="risk-panel">
            <div className={riskClassName}>{riskResult.risk_level} Risk</div>
            <p><strong>Score:</strong> {riskResult.score}</p>
            <p>{riskResult.explanation}</p>
            <small>Label: {riskResult.label}</small>
          </div>
        )}
      </SectionCard>

      <SectionCard title="Doctor Workload Meter (AI-assisted insights)">
        <label>Doctor ID</label>
        <input
          value={doctorId}
          onChange={(e) => setDoctorId(e.target.value)}
        />
        <label>Patients per Day</label>
        <input
          type="number"
          value={patientsPerDay}
          onChange={(e) => setPatientsPerDay(e.target.value)}
          min={0}
        />
        <label>Average Consultation Time (minutes)</label>
        <input
          type="number"
          value={averageConsultationMinutes}
          onChange={(e) => setAverageConsultationMinutes(e.target.value)}
          min={1}
        />
        <button onClick={fetchWorkloadPrediction}>Predict Workload</button>

        {workloadResult && (
          <div className="workload-panel">
            <p><strong>Workload Level:</strong> {workloadResult.workload_level}</p>
            <p><strong>Workload Score:</strong> {workloadResult.workload_score}</p>
            <p><strong>Complexity Factor:</strong> {workloadResult.complexity_factor}</p>
            <ul>
              {workloadResult.suggested_actions?.map((action) => (
                <li key={action}>{action}</li>
              ))}
            </ul>
            <small>Label: {workloadResult.label}</small>
          </div>
        )}
      </SectionCard>

      <AnalyticsDashboard apiBase={API_BASE} />
      <AlertPanel apiBase={API_BASE} />
    </main>
  )
}

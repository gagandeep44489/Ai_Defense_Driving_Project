import { useState } from 'react';
import AgentMonitoringPage from '../pages/AgentMonitoringPage';
import RequestValidationPage from '../pages/RequestValidationPage';
import AdminControlPage from '../pages/AdminControlPage';

const tabs = ['Agent Monitoring', 'Request Validation', 'Admin Control Panel'];

export default function App() {
  const [tab, setTab] = useState(tabs[0]);

  return (
    <main className="app">
      <h1>AGL-X Dashboard</h1>
      <div className="tabs">
        {tabs.map((item) => (
          <button key={item} className={item === tab ? 'active' : ''} onClick={() => setTab(item)}>{item}</button>
        ))}
      </div>
      {tab === 'Agent Monitoring' && <AgentMonitoringPage />}
      {tab === 'Request Validation' && <RequestValidationPage />}
      {tab === 'Admin Control Panel' && <AdminControlPage />}
    </main>
  );
}

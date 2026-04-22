import React from 'react';
import { createRoot } from 'react-dom/client';
import { DashboardPage } from './pages/DashboardPage.jsx';
import './styles.css';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <DashboardPage />
  </React.StrictMode>
);

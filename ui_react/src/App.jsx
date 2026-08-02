import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import SetupWizard from './pages/SetupWizard';
import Personnel from './pages/Personnel';
import Incidents from './pages/Incidents';
import Medical from './pages/Medical';
import Training from './pages/Training';
import PpeStock from './pages/PpeStock';
import PpeIssuance from './pages/PpeIssuance';
import Disciplinary from './pages/Disciplinary';
import PersonnelProfile from './pages/PersonnelProfile';
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:8000';

function App() {
  const [workspace, setWorkspace] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/workspace')
      .then(res => {
        setWorkspace(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="flex h-screen items-center justify-center">درحال بارگذاری...</div>;

  if (!workspace || !workspace.setup_completed) {
    return <SetupWizard onComplete={() => setWorkspace({...workspace, setup_completed: 1})} />;
  }

  return (
    <Router>
      <Layout workspace={workspace}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/personnel" element={<Personnel />} />
          <Route path="/incidents" element={<Incidents />} />
          <Route path="/medical" element={<Medical />} />
          <Route path="/training" element={<Training />} />
          <Route path="/ppe-stock" element={<PpeStock />} />
          <Route path="/ppe-issuance" element={<PpeIssuance />} />
          <Route path="/disciplinary" element={<Disciplinary />} />
          {/* Placeholder for missing routes */}
          <Route path="/profile" element={<PersonnelProfile />} />
          <Route path="/reports" element={<div className="p-8 text-center text-gray-500 font-bold text-xl bg-white rounded shadow">در حال توسعه ...</div>} />
          <Route path="/backup" element={<div className="p-8 text-center text-gray-500 font-bold text-xl bg-white rounded shadow">در حال توسعه ...</div>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

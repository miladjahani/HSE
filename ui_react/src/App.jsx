import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import SetupWizard from './pages/SetupWizard';
import axios from 'axios';

// Ensure standard backend connection
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
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

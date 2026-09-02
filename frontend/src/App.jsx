import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import MainLayout from './layouts/MainLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Leads from './pages/Leads';
import LeadDetails from './pages/LeadDetails';
import AIOutreach from './pages/AIOutreach';
import ConversationIntelligence from './pages/ConversationIntelligence';
import CRMSync from './pages/CRMSync';
import Profile from './pages/Profile';
import FollowUps from './pages/FollowUps';
import Recommendations from './pages/Recommendations';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);
  if (loading) return <div className="text-center p-5 text-light">Loading SalesGenie AI...</div>;
  if (!user) return <Navigate to="/login" replace />;
  return <MainLayout>{children}</MainLayout>;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/leads" element={<ProtectedRoute><Leads /></ProtectedRoute>} />
          <Route path="/leads/:id" element={<ProtectedRoute><LeadDetails /></ProtectedRoute>} />
          <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
          <Route path="/followups" element={<ProtectedRoute><FollowUps /></ProtectedRoute>} />
          <Route path="/outreach" element={<ProtectedRoute><AIOutreach /></ProtectedRoute>} />
          <Route path="/conversations" element={<ProtectedRoute><ConversationIntelligence /></ProtectedRoute>} />
          <Route path="/crm" element={<ProtectedRoute><CRMSync /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

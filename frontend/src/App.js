import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage.js';
import Register from './pages/Register.js';
import Login from './pages/Login.js';
import Dashboard from './pages/Dashboard.js';
import AdminDashboard from './pages/AdminDashboard.js';
import './App.css';

// Protected Route Component with optional admin check
function ProtectedRoute({ children, requireAdmin = false }) {
  const token = localStorage.getItem('access_token');

  if (!token) {
    return <Navigate to="/login" />;
  }

  if (requireAdmin) {
    const role = localStorage.getItem('user_role');
    const isStaff = localStorage.getItem('is_staff') === 'true';
    const isSuperuser = localStorage.getItem('is_superuser') === 'true';
    const isAdmin = role === 'admin' || isStaff || isSuperuser;

    if (!isAdmin) {
      return <Navigate to="/dashboard" />;
    }
  }

  return children;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute requireAdmin>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
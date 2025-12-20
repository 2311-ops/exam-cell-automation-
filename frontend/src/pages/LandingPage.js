import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/LandingPage.css';

function LandingPage() {
  const [showLogin, setShowLogin] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="landing-content">
        <h1>
          <span className="logo-icon">📚</span>
          <span className="logo-text">Exam Cell Automation</span>
        </h1>
        <p>Manage your exams, hall tickets, and results in one place</p>

        <div className="button-group">
          <button
            className="btn btn-primary"
            onClick={() => navigate('/register')}
          >
            Register
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => navigate('/login')}
          >
            Login
          </button>
        </div>

        <div className="features">
          <div className="feature">
            <h3>✓ Easy Registration</h3>
            <p>Create your account in seconds</p>
          </div>
          <div className="feature">
            <h3>✓ Exam Registration</h3>
            <p>Register for exams and get hall tickets</p>
          </div>
          <div className="feature">
            <h3>✓ View Results</h3>
            <p>Check your marks and grades instantly</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
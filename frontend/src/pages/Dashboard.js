import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, studentsAPI } from '../services/apiService';
import '../styles/Dashboard.css';

function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [exams, setExams] = useState([]);
  const [registeredExams, setRegisteredExams] = useState([]);
  const [hallTickets, setHallTickets] = useState([]);
  const [marksheets, setMarksheets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('profile');
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch user data
      const userRes = await authAPI.getMe();
      setUserData(userRes.data);

      // Fetch available exams
      const examsRes = await studentsAPI.getAvailableExams();
      setExams(examsRes.data);

      // Fetch registered exams
      const registeredRes = await studentsAPI.getRegisteredExams();
      setRegisteredExams(registeredRes.data);

      // Fetch hall tickets
      const ticketsRes = await studentsAPI.getHallTickets();
      setHallTickets(ticketsRes.data);

      // Fetch marksheets
      const marksRes = await studentsAPI.getMarksheets();
      setMarksheets(marksRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
      // Redirect to login if unauthorized
      if (err.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterExam = async (exam_id) => {
    try {
      await studentsAPI.registerExam(exam_id);
      alert('Exam registered successfully!');
      fetchData();
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to register for exam');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    navigate('/');
  };

  if (loading) {
    return <div className="dashboard-container"><div className="loading">Loading...</div></div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>📊 Student Dashboard</h1>
        <div className="header-actions">
          <span className="username">👤 {userData?.username}</span>
          <button className="btn btn-logout" onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <div className="dashboard-tabs">
        <button
          className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </button>
        <button
          className={`tab-btn ${activeTab === 'exams' ? 'active' : ''}`}
          onClick={() => setActiveTab('exams')}
        >
          Available Exams
        </button>
        <button
          className={`tab-btn ${activeTab === 'registered' ? 'active' : ''}`}
          onClick={() => setActiveTab('registered')}
        >
          My Exams
        </button>
        <button
          className={`tab-btn ${activeTab === 'tickets' ? 'active' : ''}`}
          onClick={() => setActiveTab('tickets')}
        >
          Hall Tickets
        </button>
        <button
          className={`tab-btn ${activeTab === 'marks' ? 'active' : ''}`}
          onClick={() => setActiveTab('marks')}
        >
          Results
        </button>
      </div>

      <div className="dashboard-content">
        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="tab-content">
            <h2>👤 My Profile</h2>
            {userData && (
              <div className="profile-card">
                <div className="profile-item">
                  <span className="label">Username:</span>
                  <span className="value">{userData.username}</span>
                </div>
                <div className="profile-item">
                  <span className="label">Email:</span>
                  <span className="value">{userData.email}</span>
                </div>
                <div className="profile-item">
                  <span className="label">Role:</span>
                  <span className="value">{userData.role}</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Available Exams Tab */}
        {activeTab === 'exams' && (
          <div className="tab-content">
            <h2>📝 Available Exams</h2>
            {exams.length > 0 ? (
              <div className="exams-list">
                {exams.map((exam) => (
                  <div key={exam.id} className="exam-card">
                    <h3>{exam.name}</h3>
                    <p>{exam.description}</p>
                    <div className="exam-details">
                      <span>📅 {new Date(exam.exam_date).toLocaleDateString()}</span>
                      <span>⏱️ {exam.duration_minutes} mins</span>
                      <span>📊 {exam.total_marks} marks</span>
                    </div>
                    <button
                      className="btn btn-primary"
                      onClick={() => handleRegisterExam(exam.id)}
                    >
                      Register
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <p>No exams available</p>
            )}
          </div>
        )}

        {/* My Exams Tab */}
        {activeTab === 'registered' && (
          <div className="tab-content">
            <h2>📋 My Registered Exams</h2>
            {registeredExams.length > 0 ? (
              <div className="exams-list">
                {registeredExams.map((reg) => (
                  <div key={reg.id} className="exam-card">
                    <h3>{reg.exam.name}</h3>
                    <div className="exam-details">
                      <span>📅 {new Date(reg.exam.exam_date).toLocaleDateString()}</span>
                      <span>⏱️ {reg.exam.duration_minutes} mins</span>
                    </div>
                    <div className="status">
                      Status: {reg.is_approved ? '✅ Approved' : '⏳ Pending'}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p>You haven't registered for any exams yet</p>
            )}
          </div>
        )}

        {/* Hall Tickets Tab */}
        {activeTab === 'tickets' && (
          <div className="tab-content">
            <h2>🎫 Hall Tickets</h2>
            {hallTickets.length > 0 ? (
              <div className="tickets-list">
                {hallTickets.map((ticket) => (
                  <div key={ticket.id} className="ticket-card">
                    <h3>{ticket.exam.name}</h3>
                    <div className="ticket-details">
                      <p><strong>Roll Number:</strong> {ticket.roll_number}</p>
                      <p><strong>Seat Number:</strong> {ticket.seat_number}</p>
                      <p><strong>Room Number:</strong> {ticket.room_number}</p>
                      <p><strong>Invigilator:</strong> {ticket.invigilator_name}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p>No hall tickets issued yet</p>
            )}
          </div>
        )}

        {/* Results Tab */}
        {activeTab === 'marks' && (
          <div className="tab-content">
            <h2>📊 Results</h2>
            {marksheets.length > 0 ? (
              <div className="results-list">
                {marksheets.map((mark) => (
                  <div key={mark.id} className={`result-card result-${mark.result_status.toLowerCase()}`}>
                    <h3>{mark.exam.name}</h3>
                    <div className="result-details">
                      <div className="detail-row">
                        <span>Marks:</span>
                        <span className="marks-value">{mark.marks_obtained} / {mark.total_marks}</span>
                      </div>
                      <div className="detail-row">
                        <span>Percentage:</span>
                        <span className="percentage-value">{mark.percentage?.toFixed(2)}%</span>
                      </div>
                      <div className="detail-row">
                        <span>Grade:</span>
                        <span className="grade-value">{mark.grade}</span>
                      </div>
                      <div className="detail-row">
                        <span>Status:</span>
                        <span className={`status-${mark.result_status.toLowerCase()}`}>
                          {mark.result_status}
                        </span>
                      </div>
                    </div>
                    {mark.remarks && <p className="remarks">Remarks: {mark.remarks}</p>}
                  </div>
                ))}
              </div>
            ) : (
              <p>No results published yet</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
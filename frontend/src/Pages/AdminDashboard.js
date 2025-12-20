import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, adminAPI } from '../services/apiService.js';
import '../styles/Dashboard.css';

function AdminDashboard() {
  const [me, setMe] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [users, setUsers] = useState([]);
  const [exams, setExams] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [hallTickets, setHallTickets] = useState([]);
  const [marksheets, setMarksheets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [emailSubject, setEmailSubject] = useState('');
  const [emailMessage, setEmailMessage] = useState('');
  const [emailStatus, setEmailStatus] = useState('');

  const [newExam, setNewExam] = useState({
    name: '',
    description: '',
    exam_date: '',
    duration_minutes: '',
    total_marks: '',
  });

  const navigate = useNavigate();

  useEffect(() => {
    const loadAdminData = async () => {
      try {
        setError('');
        const meRes = await authAPI.getMe();
        const user = meRes.data;

        const isAdmin =
          user.role === 'admin' || user.is_staff === true || user.is_superuser === true;

        if (!isAdmin) {
          navigate('/dashboard');
          return;
        }

        setMe(user);

        const [usersRes, examsRes, regsRes, ticketsRes, marksRes] = await Promise.all([
          adminAPI.getUsers(),
          adminAPI.getExams(),
          adminAPI.getRegistrations(),
          adminAPI.getHallTickets(),
          adminAPI.getMarksheets(),
        ]);

        setUsers(usersRes.data);
        setExams(examsRes.data);
        setRegistrations(regsRes.data);
        setHallTickets(ticketsRes.data);
        setMarksheets(marksRes.data);
      } catch (err) {
        console.error('Failed to load admin data', err);
        if (err.response?.status === 401) {
          navigate('/login');
        } else {
          setError('Failed to load admin data.');
        }
      } finally {
        setLoading(false);
      }
    };

    loadAdminData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    localStorage.removeItem('user_role');
    localStorage.removeItem('is_staff');
    localStorage.removeItem('is_superuser');
    navigate('/');
  };

  const handleSendEmail = async (e) => {
    e.preventDefault();
    setEmailStatus('');

    if (!emailSubject.trim() || !emailMessage.trim()) {
      setEmailStatus('Subject and message are required.');
      return;
    }

    try {
      const res = await adminAPI.emailStudents(emailSubject.trim(), emailMessage.trim());
      setEmailStatus(res.data?.detail || 'Email sent successfully.');
      setEmailSubject('');
      setEmailMessage('');
    } catch (err) {
      console.error('Failed to send email to students', err);
      setEmailStatus(
        err.response?.data?.detail || 'Failed to send email to students.'
      );
    }
  };

  const handleApproveRegistration = async (registrationId) => {
    try {
      await adminAPI.approveRegistration(registrationId);
      setRegistrations((prev) =>
        prev.map((reg) =>
          reg.id === registrationId ? { ...reg, is_approved: true } : reg
        )
      );
    } catch (err) {
      console.error('Failed to approve registration', err);
      alert('Failed to approve registration');
    }
  };

  const handleExamInputChange = (e) => {
    const { name, value } = e.target;
    setNewExam((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCreateExam = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        name: newExam.name,
        description: newExam.description,
        exam_date: newExam.exam_date ? new Date(newExam.exam_date).toISOString() : null,
        duration_minutes: Number(newExam.duration_minutes || 0),
        total_marks: Number(newExam.total_marks || 0),
      };

      const res = await adminAPI.createExam(payload);
      setExams((prev) => [res.data, ...prev]);
      setNewExam({ name: '', description: '', exam_date: '', duration_minutes: '', total_marks: '' });
    } catch (err) {
      console.error('Failed to create exam', err);
      alert('Failed to create exam');
    }
  };

  const handleDeleteExam = async (examId) => {
    if (!window.confirm('Delete this exam?')) return;
    try {
      await adminAPI.deleteExam(examId);
      setExams((prev) => prev.filter((exam) => exam.id !== examId));
    } catch (err) {
      console.error('Failed to delete exam', err);
      alert('Failed to delete exam');
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading admin dashboard...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>🛠️ Admin Dashboard</h1>
        <div className="header-actions">
          <span className="username">👤 {me?.username}</span>
          <button className="btn btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="dashboard-tabs">
        <button
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab-btn ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button
          className={`tab-btn ${activeTab === 'exams' ? 'active' : ''}`}
          onClick={() => setActiveTab('exams')}
        >
          Exams
        </button>
        <button
          className={`tab-btn ${activeTab === 'registrations' ? 'active' : ''}`}
          onClick={() => setActiveTab('registrations')}
        >
          Registrations
        </button>
        <button
          className={`tab-btn ${activeTab === 'halltickets' ? 'active' : ''}`}
          onClick={() => setActiveTab('halltickets')}
        >
          Hall Tickets
        </button>
        <button
          className={`tab-btn ${activeTab === 'marksheets' ? 'active' : ''}`}
          onClick={() => setActiveTab('marksheets')}
        >
          Marksheets
        </button>
        <button
          className={`tab-btn ${activeTab === 'email' ? 'active' : ''}`}
          onClick={() => setActiveTab('email')}
        >
          Email Students
        </button>
      </div>

      <div className="dashboard-content">
        {activeTab === 'overview' && (
          <div className="tab-content">
            <h2>📊 System Overview</h2>
            <div className="exams-list">
              <div className="exam-card">
                <h3>Total Users</h3>
                <p>{users.length}</p>
              </div>
              <div className="exam-card">
                <h3>Total Exams</h3>
                <p>{exams.length}</p>
              </div>
              <div className="exam-card">
                <h3>Total Registrations</h3>
                <p>{registrations.length}</p>
              </div>
              <div className="exam-card">
                <h3>Total Hall Tickets</h3>
                <p>{hallTickets.length}</p>
              </div>
              <div className="exam-card">
                <h3>Total Marksheets</h3>
                <p>{marksheets.length}</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'users' && (
          <div className="tab-content">
            <h2>👥 Users</h2>
            {users.length === 0 ? (
              <p>No users found.</p>
            ) : (
              <div className="results-list">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Staff</th>
                      <th>Superuser</th>
                      <th>Active</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((user) => (
                      <tr key={user.id}>
                        <td>{user.id}</td>
                        <td>{user.username}</td>
                        <td>{user.email}</td>
                        <td>{user.role}</td>
                        <td>{user.is_staff ? 'Yes' : 'No'}</td>
                        <td>{user.is_superuser ? 'Yes' : 'No'}</td>
                        <td>{user.is_active ? 'Yes' : 'No'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'exams' && (
          <div className="tab-content">
            <h2>📝 Manage Exams</h2>
            <form className="profile-card" onSubmit={handleCreateExam}>
              <div className="profile-item">
                <span className="label">Name</span>
                <input
                  type="text"
                  name="name"
                  value={newExam.name}
                  onChange={handleExamInputChange}
                  required
                />
              </div>
              <div className="profile-item">
                <span className="label">Description</span>
                <textarea
                  name="description"
                  value={newExam.description}
                  onChange={handleExamInputChange}
                />
              </div>
              <div className="profile-item">
                <span className="label">Exam Date & Time</span>
                <input
                  type="datetime-local"
                  name="exam_date"
                  value={newExam.exam_date}
                  onChange={handleExamInputChange}
                  required
                />
              </div>
              <div className="profile-item">
                <span className="label">Duration (minutes)</span>
                <input
                  type="number"
                  name="duration_minutes"
                  value={newExam.duration_minutes}
                  onChange={handleExamInputChange}
                  required
                />
              </div>
              <div className="profile-item">
                <span className="label">Total Marks</span>
                <input
                  type="number"
                  name="total_marks"
                  value={newExam.total_marks}
                  onChange={handleExamInputChange}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary">
                Create Exam
              </button>
            </form>

            <h3 style={{ marginTop: '2rem' }}>Existing Exams</h3>
            {exams.length === 0 ? (
              <p>No exams found.</p>
            ) : (
              <div className="exams-list">
                {exams.map((exam) => (
                  <div key={exam.id} className="exam-card">
                    <h3>{exam.name}</h3>
                    <p>{exam.description}</p>
                    <div className="exam-details">
                      <span>
                        📅 {exam.exam_date ? new Date(exam.exam_date).toLocaleString() : 'N/A'}
                      </span>
                      <span>⏱️ {exam.duration_minutes} mins</span>
                      <span>📊 {exam.total_marks} marks</span>
                    </div>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDeleteExam(exam.id)}
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'registrations' && (
          <div className="tab-content">
            <h2>📋 Student Exam Registrations</h2>
            {registrations.length === 0 ? (
              <p>No registrations yet.</p>
            ) : (
              <div className="results-list">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Student</th>
                      <th>Exam</th>
                      <th>Registered At</th>
                      <th>Approved</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {registrations.map((reg) => (
                      <tr key={reg.id}>
                        <td>{reg.id}</td>
                        <td>{reg.student_username}</td>
                        <td>{reg.exam_name}</td>
                        <td>{new Date(reg.registered_at).toLocaleString()}</td>
                        <td>{reg.is_approved ? 'Yes' : 'No'}</td>
                        <td>
                          {!reg.is_approved && (
                            <button
                              className="btn btn-primary"
                              onClick={() => handleApproveRegistration(reg.id)}
                            >
                              Approve
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'halltickets' && (
          <div className="tab-content">
            <h2>🎫 Hall Tickets</h2>
            {hallTickets.length === 0 ? (
              <p>No hall tickets issued.</p>
            ) : (
              <div className="results-list">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Student</th>
                      <th>Exam</th>
                      <th>Roll Number</th>
                      <th>Seat</th>
                      <th>Room</th>
                      <th>Invigilator</th>
                    </tr>
                  </thead>
                  <tbody>
                    {hallTickets.map((t) => (
                      <tr key={t.id}>
                        <td>{t.id}</td>
                        <td>{t.student_username}</td>
                        <td>{t.exam_name}</td>
                        <td>{t.roll_number}</td>
                        <td>{t.seat_number}</td>
                        <td>{t.room_number}</td>
                        <td>{t.invigilator_name}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'marksheets' && (
          <div className="tab-content">
            <h2>📑 Marksheets</h2>
            {marksheets.length === 0 ? (
              <p>No marksheets found.</p>
            ) : (
              <div className="results-list">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Student</th>
                      <th>Exam</th>
                      <th>Marks</th>
                      <th>Percentage</th>
                      <th>Grade</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {marksheets.map((m) => (
                      <tr key={m.id}>
                        <td>{m.id}</td>
                        <td>{m.student_username}</td>
                        <td>{m.exam_name}</td>
                        <td>
                          {m.marks_obtained} / {m.total_marks}
                        </td>
                        <td>{m.percentage?.toFixed(2)}%</td>
                        <td>{m.grade}</td>
                        <td>{m.result_status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'email' && (
          <div className="tab-content">
            <h2>📧 Email All Registered Students</h2>
            <div className="profile-card">
              {emailStatus && (
                <div
                  className={
                    emailStatus.toLowerCase().includes('failed')
                      ? 'alert alert-error'
                      : 'alert alert-success'
                  }
                >
                  {emailStatus}
                </div>
              )}
              <form onSubmit={handleSendEmail}>
                <div className="profile-item">
                  <span className="label">Subject</span>
                  <input
                    type="text"
                    value={emailSubject}
                    onChange={(e) => setEmailSubject(e.target.value)}
                    placeholder="Enter email subject"
                  />
                </div>
                <div className="profile-item" style={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                  <span className="label" style={{ marginBottom: '8px' }}>Message</span>
                  <textarea
                    value={emailMessage}
                    onChange={(e) => setEmailMessage(e.target.value)}
                    placeholder="Enter email body to send to all students"
                    rows={6}
                    style={{ width: '100%' }}
                  />
                </div>
                <button type="submit" className="btn btn-primary">
                  Emai sent to Students
                </button>
              </form>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default AdminDashboard;

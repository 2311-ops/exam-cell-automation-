import React, { useState, useEffect } from 'react';

export function Dashboard({ token, username, onLogout }){
  const [activeTab, setActiveTab] = useState('halltickets');
  const [halltickets, setHalltickets] = useState([]);
  const [marksheets, setMarksheets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [createExamName, setCreateExamName] = useState('');

  useEffect(() => {
    loadHalltickets();
  }, []);

  async function loadHalltickets() {
    setLoading(true);
    setError('');
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/halltickets/', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await resp.json();
      if(resp.ok) {
        setHalltickets(Array.isArray(data) ? data : []);
      } else {
        setError('Failed to load hall tickets');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadMarksheets() {
    setLoading(true);
    setError('');
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/marksheets/', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await resp.json();
      if(resp.ok) {
        setMarksheets(Array.isArray(data) ? data : []);
      } else {
        setError('Failed to load marksheets');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  async function createHallticket(e) {
    e.preventDefault();
    if(!createExamName.trim()) {
      setError('Please enter exam name');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/halltickets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ exam_name: createExamName })
      });
      const data = await resp.json();
      if(resp.ok) {
        setCreateExamName('');
        loadHalltickets();
      } else {
        setError(data.detail || 'Failed to create hall ticket');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  const navStyle = {
    display: 'flex',
    borderBottom: '2px solid #ddd',
    marginBottom: 20,
    gap: 0
  };

  const navButtonStyle = (isActive) => ({
    padding: '10px 20px',
    border: 'none',
    backgroundColor: isActive ? '#007bff' : '#f5f5f5',
    color: isActive ? 'white' : '#333',
    cursor: 'pointer',
    fontSize: 14,
    fontWeight: isActive ? 'bold' : 'normal',
    borderRadius: 0
  });

  return (
    <div style={{ maxWidth: 900, margin: '0 auto' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 30,
        paddingBottom: 15,
        borderBottom: '1px solid #ddd'
      }}>
        <div>
          <h2 style={{margin: 0}}>Welcome, {username}</h2>
        </div>
        <button
          onClick={onLogout}
          style={{
            padding: '8px 16px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Logout
        </button>
      </div>

      {error && (
        <div style={{
          padding: 15,
          marginBottom: 20,
          backgroundColor: '#fee',
          color: '#c33',
          borderRadius: 4
        }}>
          {error}
        </div>
      )}

      <div style={navStyle}>
        <button
          style={navButtonStyle(activeTab === 'halltickets')}
          onClick={() => {
            setActiveTab('halltickets');
            loadHalltickets();
          }}
        >
          Hall Tickets
        </button>
        <button
          style={navButtonStyle(activeTab === 'marksheets')}
          onClick={() => {
            setActiveTab('marksheets');
            loadMarksheets();
          }}
        >
          Marksheets
        </button>
      </div>

      {activeTab === 'halltickets' && (
        <div>
          <div style={{
            backgroundColor: '#f9f9f9',
            padding: 20,
            borderRadius: 4,
            marginBottom: 20
          }}>
            <h3 style={{marginTop: 0}}>Create Hall Ticket</h3>
            <form onSubmit={createHallticket} style={{display: 'flex', gap: 10}}>
              <input
                type="text"
                placeholder="Enter exam name"
                value={createExamName}
                onChange={e => setCreateExamName(e.target.value)}
                style={{
                  flex: 1,
                  padding: 8,
                  border: '1px solid #ccc',
                  borderRadius: 4
                }}
              />
              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#28a745',
                  color: 'white',
                  border: 'none',
                  borderRadius: 4,
                  cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.7 : 1
                }}
              >
                {loading ? 'Creating...' : 'Create'}
              </button>
            </form>
          </div>

          <div>
            <h3>Your Hall Tickets</h3>
            {loading && !halltickets.length ? (
              <p>Loading...</p>
            ) : halltickets.length > 0 ? (
              <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                border: '1px solid #ddd'
              }}>
                <thead>
                  <tr style={{backgroundColor: '#f5f5f5', fontWeight: 'bold'}}>
                    <th style={{padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd'}}>Exam Name</th>
                    <th style={{padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd'}}>Seat No</th>
                    <th style={{padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd'}}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {halltickets.map((ticket, idx) => (
                    <tr key={idx} style={{borderBottom: '1px solid #ddd'}}>
                      <td style={{padding: 12}}>{ticket.exam_name}</td>
                      <td style={{padding: 12}}>{ticket.seat_no || '-'}</td>
                      <td style={{padding: 12}}>Active</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p style={{color: '#666'}}>No hall tickets found. Create one to get started.</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'marksheets' && (
        <div>
          <h3>Your Marksheets</h3>
          {loading && !marksheets.length ? (
            <p>Loading...</p>
          ) : marksheets.length > 0 ? (
            <table style={{
              width: '100%',
              borderCollapse: 'collapse',
              border: '1px solid #ddd'
            }}>
              <thead>
                <tr style={{backgroundColor: '#f5f5f5', fontWeight: 'bold'}}>
                  <th style={{padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd'}}>Subject</th>
                  <th style={{padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd'}}>Marks</th>
                  <th style={{padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd'}}>Grade</th>
                </tr>
              </thead>
              <tbody>
                {marksheets.map((sheet, idx) => (
                  <tr key={idx} style={{borderBottom: '1px solid #ddd'}}>
                    <td style={{padding: 12}}>{sheet.subject || '-'}</td>
                    <td style={{padding: 12}}>{sheet.marks || '-'}</td>
                    <td style={{padding: 12}}>{sheet.grade || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p style={{color: '#666'}}>No marksheets available yet.</p>
          )}
        </div>
      )}
    </div>
  );
}

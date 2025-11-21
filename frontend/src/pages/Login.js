import React, { useState } from 'react';

export function Login({ onLogin }){
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function doLogin(e){
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const resp = await fetch('http://127.0.0.1:8000/api/accounts/token/', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({username, password})
      });
      const data = await resp.json();
      
      if(resp.ok){
        onLogin(data.access, username);
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      maxWidth: 400,
      margin: '50px auto',
      padding: 30,
      border: '1px solid #ddd',
      borderRadius: 8,
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <h2 style={{textAlign: 'center'}}>Login</h2>
      
      {error && (
        <div style={{
          padding: 10,
          marginBottom: 15,
          backgroundColor: '#fee',
          color: '#c33',
          borderRadius: 4,
          fontSize: 14
        }}>
          {error}
        </div>
      )}

      <form onSubmit={doLogin}>
        <div style={{marginBottom: 15}}>
          <label style={{display: 'block', marginBottom: 5, fontWeight: 'bold'}}>Username</label>
          <input 
            type="text"
            placeholder="Enter your username" 
            value={username} 
            onChange={e=>setUsername(e.target.value)}
            style={{
              width: '100%',
              padding: 8,
              border: '1px solid #ccc',
              borderRadius: 4,
              boxSizing: 'border-box'
            }}
            required
          /> 
        </div>

        <div style={{marginBottom: 20}}>
          <label style={{display: 'block', marginBottom: 5, fontWeight: 'bold'}}>Password</label>
          <input 
            type="password" 
            placeholder="Enter your password"
            value={password} 
            onChange={e=>setPassword(e.target.value)}
            style={{
              width: '100%',
              padding: 8,
              border: '1px solid #ccc',
              borderRadius: 4,
              boxSizing: 'border-box'
            }}
            required
          /> 
        </div>

        <button 
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: 10,
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: 4,
            fontSize: 16,
            fontWeight: 'bold',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  )
}

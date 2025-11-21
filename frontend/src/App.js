import React, { useState } from 'react';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';

export default function App(){
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState('');

  const handleLogin = (accessToken, user) => {
    setToken(accessToken);
    setUsername(user);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setToken(null);
    setUsername('');
    setIsLoggedIn(false);
  };

  return (
    <div style={{padding:20, fontFamily:'Arial, sans-serif'}}>
      <h1>Examcell</h1>
      {isLoggedIn ? (
        <Dashboard token={token} username={username} onLogout={handleLogout} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  )
}

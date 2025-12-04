import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div style={{ backgroundColor: "#1e3a5f", minHeight: "100vh" }}>
      <div>
        <a href="https://vite.dev" target="_blank" rel="noreferrer">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank" rel="noreferrer">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <div className="auth-links">
        <a href="/login" className="auth-link">Login</a>
        <a href="/register" className="auth-link">Register</a>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  )
}

export default App

.auth-links {
  display: flex;
  gap: 16px;
  margin: 24px 0;
}

.auth-link {
  padding: 10px 20px;
  font-size: 16px;
  text-decoration: none;
  color: white;
  background-color: #333;
  border-radius: 6px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.auth-link:hover {
  background-color: #26ff00;
  color: #1e3a5f;
  transform: scale(1.15);
}

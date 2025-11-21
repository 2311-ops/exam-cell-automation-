import React, { useState } from 'react';

export function Register(){
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  async function doRegister(e){
    e.preventDefault();
    const resp = await fetch('http://127.0.0.1:8000/api/accounts/register/', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({username, email, password, role:'student'})
    });
    const data = await resp.json();
    if(resp.ok){
      alert('Registered: '+data.username);
    } else {
      alert('Register failed: '+ JSON.stringify(data));
    }
  }

  return (
    <div style={{border:'1px solid #ddd', padding:10, marginBottom:10}}>
      <h3>Register</h3>
      <form onSubmit={doRegister}>
        <input placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} /> <br/>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} /> <br/>
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} /> <br/>
        <button type="submit">Register</button>
      </form>
    </div>
  )
}

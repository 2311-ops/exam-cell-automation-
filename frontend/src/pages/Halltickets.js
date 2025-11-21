import React, { useState } from 'react';

export function Halltickets(){
  const [exam, setExam] = useState('');
  const [access, setAccess] = useState('');
  const [tickets, setTickets] = useState([]);

  async function createTicket(e){
    e.preventDefault();
    const resp = await fetch('http://127.0.0.1:8000/api/halltickets/', {
      method: 'POST',
      headers: {'Content-Type':'application/json','Authorization': 'Bearer '+access},
      body: JSON.stringify({exam_name: exam})
    });
    const data = await resp.json();
    if(resp.ok){
      alert('Hallticket created: '+data.seat_no);
    } else {
      alert('Create failed: '+JSON.stringify(data));
    }
  }

  async function listTickets(){
    const resp = await fetch('http://127.0.0.1:8000/api/halltickets/', {headers: {'Authorization': 'Bearer '+access}});
    const data = await resp.json();
    if(resp.ok) setTickets(data);
    else alert('List failed: '+JSON.stringify(data));
  }

  return (
    <div style={{border:'1px solid #ddd', padding:10}}>
      <h3>Halltickets</h3>
      <input placeholder="access token" value={access} onChange={e=>setAccess(e.target.value)} style={{width:'100%'}} />
      <form onSubmit={createTicket}>
        <input placeholder="exam name" value={exam} onChange={e=>setExam(e.target.value)} />
        <button type="submit">Create Hallticket</button>
      </form>
      <button onClick={listTickets}>List Tickets</button>
      <pre>{JSON.stringify(tickets, null, 2)}</pre>
    </div>
  )
}

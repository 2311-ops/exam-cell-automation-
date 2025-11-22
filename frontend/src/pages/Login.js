export async function initLogin(username, password) {
  const msg = document.getElementById('loginMsg');
  msg.textContent = '';
  if (!username || !password) {
    msg.textContent = 'Enter username and password';
    return false;
  }

  try {
    // Attempt to call backend login endpoint
    const resp = await fetch('http://localhost:8000/api/accounts/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!resp.ok) {
      try {
        const err = await resp.json();
        msg.textContent = 'Login failed: ' + (err.detail || JSON.stringify(err));
      } catch (e) {
        msg.textContent = 'Login failed: ' + resp.statusText;
      }
      return false;
    }
    const data = await resp.json();
    // server returns 'access' and 'refresh' fields
    if (data.access) {
      localStorage.setItem('exam_token', data.access);
      msg.textContent = 'Logged in';
      return true;
    }
    msg.textContent = 'Login succeeded but no token returned.';
    return false;
  } catch (err) {
    msg.textContent = 'Network error: ' + err.message;
    return false;
  }
}

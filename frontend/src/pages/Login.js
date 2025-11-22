export async function initLogin(username, password) {
  const msg = document.getElementById('loginMsg');
  msg.textContent = '';
  if (!username || !password) {
    msg.textContent = 'Enter username and password';
    return false;
  }

  try {
    // Attempt to call backend token endpoint (adjust origin if needed)
    const resp = await fetch('http://localhost:8000/api/accounts/token/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!resp.ok) {
      msg.textContent = 'Login failed: ' + resp.statusText;
      return false;
    }
    const data = await resp.json();
    localStorage.setItem('exam_token', data.access);
    msg.textContent = 'Logged in';
    return true;
  } catch (err) {
    msg.textContent = 'Network error: ' + err.message;
    return false;
  }
}

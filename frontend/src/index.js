import { initLogin } from './pages/Login.js';
import { initDashboard } from './pages/Dashboard.js';

const btnLogin = document.getElementById('btnLogin');
const btnLogout = document.getElementById('btnLogout');

btnLogin.addEventListener('click', async () => {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const ok = await initLogin(username, password);
  if (ok) {
    document.getElementById('login').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    initDashboard();
  }
});

btnLogout.addEventListener('click', () => {
  localStorage.removeItem('exam_token');
  document.getElementById('dashboard').classList.add('hidden');
  document.getElementById('login').classList.remove('hidden');
});

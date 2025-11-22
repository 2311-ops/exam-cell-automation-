export function initDashboard() {
  const content = document.getElementById('dashboardContent');
  const token = localStorage.getItem('exam_token');
  if (!token) {
    content.textContent = 'No token found. Please login.';
    return;
  }

  content.innerHTML = '';

  const info = document.createElement('div');
  info.textContent = 'Welcome! Token present (hidden).';
  content.appendChild(info);

  const actions = document.createElement('div');
  const btnGetExams = document.createElement('button');
  btnGetExams.textContent = 'List available exams';
  btnGetExams.addEventListener('click', async () => {
    try {
      const res = await fetch('http://localhost:8000/api/exams/', {
        headers: { Authorization: 'Bearer ' + token }
      });
      const data = await res.json();
      const pre = document.createElement('pre');
      pre.textContent = JSON.stringify(data, null, 2);
      content.appendChild(pre);
    } catch (e) {
      content.appendChild(document.createTextNode('Error: ' + e.message));
    }
  });
  actions.appendChild(btnGetExams);
  content.appendChild(actions);
}

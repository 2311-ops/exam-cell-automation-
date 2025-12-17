import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const apiService = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
apiService.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
<<<<<<< HEAD
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

=======

  // Don't attach token for login/register
  if (
    !config.url.includes('/accounts/login/') &&
    !config.url.includes('/accounts/register/')
  ) {
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }

  return config;
});


>>>>>>> b93a8b449bb198c041389dc301d09512a056b035
export const authAPI = {
  register: (username, email, password, role = 'student') =>
    apiService.post('/accounts/register/', { username, email, password, role }),
  
  login: (username, password) =>
    apiService.post('/accounts/login/', { username, password }),
  
  getMe: () =>
    apiService.get('/accounts/me/'),
};

export const studentsAPI = {
  getAvailableExams: () =>
    apiService.get('/students/exams/available/'),
  
  registerExam: (exam_id) =>
    apiService.post('/students/exams/register/', { exam_id }),
  
  getRegisteredExams: () =>
    apiService.get('/students/exams/registered/'),
  
  getHallTickets: () =>
    apiService.get('/students/hallticket/'),
  
  getHallTicket: (exam_id) =>
    apiService.get(`/students/hallticket/${exam_id}/`),
  
  getMarksheets: () =>
    apiService.get('/students/marksheet/'),
  
  getMarksheet: (exam_id) =>
    apiService.get(`/students/marksheet/${exam_id}/`),
};

<<<<<<< HEAD
export default apiService;
=======
export default apiService;
>>>>>>> b93a8b449bb198c041389dc301d09512a056b035

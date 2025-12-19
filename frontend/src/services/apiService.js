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

// Admin-specific APIs that mirror Django admin capabilities
export const adminAPI = {
  // Users
  getUsers: () => apiService.get('/admin/users/'),
  updateUser: (userId, data) => apiService.patch(`/admin/users/${userId}/`, data),

  // Exams
  getExams: () => apiService.get('/admin/exams/'),
  createExam: (data) => apiService.post('/admin/exams/', data),
  updateExam: (examId, data) => apiService.patch(`/admin/exams/${examId}/`, data),
  deleteExam: (examId) => apiService.delete(`/admin/exams/${examId}/`),

  // Student exam registrations
  getRegistrations: () => apiService.get('/admin/registrations/'),
  approveRegistration: (registrationId) =>
    apiService.patch(`/admin/registrations/${registrationId}/`, { is_approved: true }),

  // Hall tickets
  getHallTickets: () => apiService.get('/admin/halltickets/'),
  createHallTicket: (data) => apiService.post('/admin/halltickets/', data),
  deleteHallTicket: (hallTicketId) =>
    apiService.delete(`/admin/halltickets/${hallTicketId}/`),

  // Marksheets
  getMarksheets: () => apiService.get('/admin/marksheets/'),
  createMarksheet: (data) => apiService.post('/admin/marksheets/', data),
  updateMarksheet: (marksheetId, data) =>
    apiService.patch(`/admin/marksheets/${marksheetId}/`, data),
  deleteMarksheet: (marksheetId) =>
    apiService.delete(`/admin/marksheets/${marksheetId}/`),

  // Email all registered students
  emailStudents: (subject, message) =>
    apiService.post('/admin/email/students/', { subject, message }),
};

export default apiService;
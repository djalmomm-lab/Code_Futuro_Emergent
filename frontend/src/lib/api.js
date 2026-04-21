import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cf_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('cf_token');
      localStorage.removeItem('cf_user');
    }
    return Promise.reject(err);
  }
);

// Auth
export const authApi = {
  register: (data) => api.post('/auth/register', data).then((r) => r.data),
  login: (data) => api.post('/auth/login', data).then((r) => r.data),
  me: () => api.get('/auth/me').then((r) => r.data),
};

// Onboarding
export const onboardApi = {
  save: (data) => api.post('/onboard', data).then((r) => r.data),
};

// Progress
export const progressApi = {
  get: () => api.get('/progress').then((r) => r.data),
  completeLesson: (payload) => api.post('/progress/complete', payload).then((r) => r.data),
  consumeEnergy: () => api.post('/energy/consume').then((r) => r.data),
};

// Leaderboard
export const leaderboardApi = {
  get: (period = 'week') => api.get(`/leaderboard?period=${period}`).then((r) => r.data),
};

// Privacy
export const privacyApi = {
  export: () => api.get('/privacy/export').then((r) => r.data),
  delete: () => api.delete('/privacy/delete').then((r) => r.data),
};

export const saveAuth = (data) => {
  localStorage.setItem('cf_token', data.token);
  localStorage.setItem('cf_user', JSON.stringify(data.user));
};

export const getStoredUser = () => {
  try { return JSON.parse(localStorage.getItem('cf_user') || 'null'); } catch { return null; }
};

export const isAuthed = () => !!localStorage.getItem('cf_token');

export const logout = () => {
  localStorage.removeItem('cf_token');
  localStorage.removeItem('cf_user');
};

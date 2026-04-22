import axios from 'axios';

// NOTE (security tradeoff): We currently persist the JWT in localStorage.
// This is a conscious MVP tradeoff — it's simple and survives page reloads
// without requiring cookie/CORS changes on the backend. It is vulnerable to
// XSS, so we mitigate by:
//   - Sanitizing user-rendered content (React escapes by default)
//   - Avoiding dangerouslySetInnerHTML
//   - Validating inputs on the backend
// Roadmap: migrate to httpOnly + SameSite=Strict cookies with /api/auth/refresh
// when we add subscriptions / store sensitive data beyond learning progress.

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

// Paths / Lessons (from DB)
export const pathsApi = {
  list: () => api.get('/tracks').then((r) => r.data),
  get: (slug) => api.get(`/paths/${slug}`).then((r) => r.data),
};

export const lessonsApi = {
  get: (slug) => api.get(`/lessons/${slug}`).then((r) => r.data),
};

// Privacy
export const privacyApi = {
  export: () => api.get('/privacy/export').then((r) => r.data),
  delete: () => api.delete('/privacy/delete').then((r) => r.data),
};

export const getErrorMessage = (err) => {
  const detail = err?.response?.data?.detail;
  if (!detail) return err?.message || 'Erro inesperado';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map((d) => d.msg || JSON.stringify(d)).join(', ');
  return JSON.stringify(detail);
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

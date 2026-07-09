import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Future API endpoints
export const predictionAPI = {
  predict: (formData) => api.post('/predict', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  getHistory: () => api.get('/predictions/history'),
  getStats: () => api.get('/predictions/stats'),
};

export const modelAPI = {
  getMetrics: () => api.get('/models/metrics'),
  getComparison: () => api.get('/models/comparison'),
};

export const datasetAPI = {
  getStats: () => api.get('/datasets/stats'),
};

export default api;

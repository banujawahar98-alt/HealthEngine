import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('mindcare_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const detail = error.response?.data?.detail;
    const customError = {
      success: false,
      message:
        (typeof detail === 'object' ? detail?.message : detail) ||
        error.response?.data?.message ||
        error.message ||
        'Network error occurred. Please check server connection.',
      error_code: (typeof detail === 'object' ? detail?.error_code : null) || 'NETWORK_ERROR'
    };
    if (error.response?.status === 401) {
      localStorage.removeItem('mindcare_token');
    }
    return Promise.reject(customError);
  }
);

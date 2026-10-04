import { api } from './api';

export const authService = {
  async register(data: any) {
    return await api.post('/api/auth/register', data);
  },

  async login(data: any) {
    return await api.post('/api/auth/login', data);
  },

  async getMe() {
    return await api.get('/api/auth/me');
  },

  async changePassword(data: any) {
    return await api.put('/api/auth/change-password', data);
  },

  async deleteAccount() {
    return await api.delete('/api/auth/account');
  },

  async updateProfile(data: any) {
    return await api.put('/api/users/profile', data);
  },

  async exportData() {
    return await api.get('/api/users/export-data');
  }
};

import { api } from './api';

export const dashboardService = {
  async getSummary() {
    return await api.get('/api/dashboard/summary');
  },

  async getTrends() {
    return await api.get('/api/dashboard/trends');
  }
};

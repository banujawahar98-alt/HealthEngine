import { api } from './api';

export const adminService = {
  async getAnalytics() {
    return await api.get('/api/admin/analytics');
  },

  async createResource(data: any) {
    return await api.post('/api/admin/resources', data);
  },

  async updateResource(id: string, data: any) {
    return await api.put(`/api/admin/resources/${id}`, data);
  },

  async deleteResource(id: string) {
    return await api.delete(`/api/admin/resources/${id}`);
  },

  async createProfessional(data: any) {
    return await api.post('/api/admin/professionals', data);
  },

  async updateProfessional(id: string, data: any) {
    return await api.put(`/api/admin/professionals/${id}`, data);
  },

  async deleteProfessional(id: string) {
    return await api.delete(`/api/admin/professionals/${id}`);
  },

  async createCrisisResource(data: any) {
    return await api.post('/api/admin/crisis-resources', data);
  },

  async deleteCrisisResource(id: string) {
    return await api.delete(`/api/admin/crisis-resources/${id}`);
  }
};

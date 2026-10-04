import { api } from './api';

export const resourceService = {
  async getResources(category?: string, tag?: string, search?: string) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (tag) params.append('tag', tag);
    if (search) params.append('search', search);
    return await api.get(`/api/resources?${params.toString()}`);
  },

  async getResourceById(id: string) {
    return await api.get(`/api/resources/${id}`);
  }
};

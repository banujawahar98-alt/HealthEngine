import { api } from './api';

export const crisisService = {
  async getCrisisResources(country?: string) {
    const params = new URLSearchParams();
    if (country) params.append('country', country);
    return await api.get(`/api/crisis-resources?${params.toString()}`);
  }
};

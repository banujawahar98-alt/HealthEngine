import { api } from './api';

export const professionalService = {
  async getProfessionals(specialization?: string, location?: string, mode?: string, search?: string) {
    const params = new URLSearchParams();
    if (specialization) params.append('specialization', specialization);
    if (location) params.append('location', location);
    if (mode) params.append('mode', mode);
    if (search) params.append('search', search);
    return await api.get(`/api/professionals?${params.toString()}`);
  },

  async getProfessionalById(id: string) {
    return await api.get(`/api/professionals/${id}`);
  }
};

import { api } from './api';

export const moodService = {
  async getMoodEntries() {
    return await api.get('/api/mood');
  },

  async addMoodEntry(data: { mood: number; stress_level: number; energy_level: number; sleep_hours: number; note?: string }) {
    return await api.post('/api/mood', data);
  },

  async updateMoodEntry(id: string, data: any) {
    return await api.put(`/api/mood/${id}`, data);
  },

  async deleteMoodEntry(id: string) {
    return await api.delete(`/api/mood/${id}`);
  }
};

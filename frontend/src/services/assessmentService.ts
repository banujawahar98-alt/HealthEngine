import { api } from './api';

export const assessmentService = {
  async getAssessments() {
    return await api.get('/api/assessments');
  },

  async getAssessment(id: string) {
    return await api.get(`/api/assessments/${id}`);
  },

  async submitAssessment(id: string, responses: Record<number, number>) {
    return await api.post(`/api/assessments/${id}/submit`, { responses, ack_consent: true });
  },

  async getHistory() {
    return await api.get('/api/assessments/history');
  },

  async getResult(id: string) {
    return await api.get(`/api/assessment-results/${id}`);
  },

  async downloadPdf(id: string, filename: string) {
    const token = localStorage.getItem('mindcare_token');
    const response = await fetch(`http://localhost:8000/api/assessment-results/${id}/pdf`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    if (!response.ok) throw new Error('Failed to download PDF report');
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  }
};

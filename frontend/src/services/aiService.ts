import { api } from './api';

export const aiService = {
  async sendMessage(message: string, conversation_id?: string) {
    return await api.post('/api/ai/chat', { message, conversation_id });
  },

  async getConversations() {
    return await api.get('/api/ai/conversations');
  },

  async getConversationMessages(id: string) {
    return await api.get(`/api/ai/conversations/${id}`);
  },

  async deleteConversation(id: string) {
    return await api.delete(`/api/ai/conversations/${id}`);
  }
};

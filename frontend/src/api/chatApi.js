import axios from 'axios';

// API base URL - make sure this matches your backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

const chatApi = {
  // Send message to chatbot
  sendMessage: async (message, conversationHistory = []) => {
    try {
      console.log('Sending to:', `${API_BASE_URL}/api/chat/message`); // Debug log
      
      const response = await axios.post(
        `${API_BASE_URL}/api/chat/message`, // Correct - full path
        {
          message: message,
          history: conversationHistory
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 30000 // 30 seconds timeout
        }
      );
      
      return response.data;
    } catch (error) {
      console.error('Chat API Error:', error);
      
      if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        throw new Error('Cannot connect to server. Please ensure the backend is running on port 3000.');
      }
      
      if (error.response) {
        throw new Error(error.response.data.message || 'Server error occurred');
      }
      
      throw new Error(error.message || 'Network error occurred');
    }
  },

  // Test connection
  testConnection: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`, {
        timeout: 5000
      });
      return response.data;
    } catch (error) {
      console.error('Connection test failed:', error);
      throw error;
    }
  }
};

export default chatApi;

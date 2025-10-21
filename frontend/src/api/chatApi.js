import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

const chatApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

/**
 * Ask a question to the chatbot
 * @param {string} question - The user's question
 * @returns {Promise} Response with answer
 */
export const askQuestion = async (question) => {
  try {
    const response = await chatApi.post('/chat/ask', { question });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.message || 'Server error occurred');
    } else if (error.request) {
      // Request made but no response
      throw new Error('Cannot connect to server. Please ensure the backend is running on port 3000.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Get chat history
 * @param {number} limit - Number of messages to retrieve
 * @returns {Promise} Array of chat messages
 */
export const getChatHistory = async (limit = 50) => {
  try {
    const response = await chatApi.get(`/chat/history?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

export default chatApi;

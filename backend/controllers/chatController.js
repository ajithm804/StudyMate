import axios from 'axios';
import ChatHistory from '../models/userModel.js';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5000';

/**
 * Handle chat question from frontend
 */
export const askChatbot = async (req, res) => {
  try {
    const { question } = req.body;

    // Validation
    if (!question || question.trim().length === 0) {
      return res.status(400).json({
        status: 'error',
        message: 'Question cannot be empty'
      });
    }

    console.log(`Processing question: ${question.substring(0, 100)}...`);

    // Call Python AI service
    const response = await axios.post(`${AI_SERVICE_URL}/ask`, {
      question: question
    }, {
      timeout: 30000, // 30 second timeout
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const answer = response.data.answer;

    // Optionally save to database
    try {
      if (ChatHistory) {
        await ChatHistory.create({
          question,
          answer,
          timestamp: new Date()
        });
      }
    } catch (dbError) {
      console.log('Database save skipped:', dbError.message);
    }

    // Return answer
    res.json({
      status: 'success',
      question,
      answer,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error in askChatbot:', error.message);

    // Handle specific error cases
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        status: 'error',
        message: 'AI service is not available. Please ensure the Python service is running on port 5000.'
      });
    }

    if (error.response) {
      return res.status(error.response.status).json({
        status: 'error',
        message: error.response.data.detail || 'AI service error'
      });
    }

    res.status(500).json({
      status: 'error',
      message: 'Failed to process question',
      details: error.message
    });
  }
};

/**
 * Get chat history (optional feature)
 */
export const getChatHistory = async (req, res) => {
  try {
    if (!ChatHistory) {
      return res.json({
        status: 'success',
        history: [],
        message: 'Chat history not available (MongoDB not configured)'
      });
    }

    const limit = parseInt(req.query.limit) || 50;
    const history = await ChatHistory.find()
      .sort({ timestamp: -1 })
      .limit(limit)
      .lean();

    res.json({
      status: 'success',
      history,
      count: history.length
    });

  } catch (error) {
    console.error('Error fetching history:', error);
    res.status(500).json({
      status: 'error',
      message: 'Failed to fetch chat history'
    });
  }
};

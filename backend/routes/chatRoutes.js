import express from 'express';
import axios from 'axios';

const router = express.Router();

// AI Service URL
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5000';

// POST /api/chat/message
router.post('/message', async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    if (!message || message.trim() === '') {
      return res.status(400).json({
        status: 'error',
        message: 'Message is required'
      });
    }

    console.log(`📨 Received message: ${message.substring(0, 50)}...`);

    const aiResponse = await axios.post(
      `${AI_SERVICE_URL}/ask`,
      { 
        question: message.trim()
      },
      { 
        timeout: 30000,
        headers: { 'Content-Type': 'application/json' }
      }
    );

    console.log('✅ AI response:', aiResponse.data);

    // AI service returns {answer: "...", status: "..."}
    res.json({
      status: 'success',
      data: {
        response: aiResponse.data.answer || aiResponse.data, // Extract answer field
        sources: []
      }
    });

  } catch (error) {
    console.error('❌ Chat route error:', error.message);

    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        status: 'error',
        message: 'AI service is not available. Please ensure it is running on port 5000.'
      });
    }

    res.status(500).json({
      status: 'error',
      message: error.response?.data?.detail || error.message || 'Failed to process your request'
    });
  }
});

// GET /api/chat/test
router.get('/test', (req, res) => {
  res.json({
    status: 'success',
    message: 'Chat routes are working'
  });
});

export default router;

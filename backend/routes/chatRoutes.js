import express from 'express';
import { askChatbot, getChatHistory } from '../controllers/chatController.js';

const router = express.Router();

// POST /api/chat/ask - Ask a question
router.post('/ask', askChatbot);

// GET /api/chat/history - Get chat history (optional, requires MongoDB)
router.get('/history', getChatHistory);

export default router;

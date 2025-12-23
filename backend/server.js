import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import mongoose from 'mongoose';
import chatRoutes from './routes/chatRoutes.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware - CORS must come first
app.use(cors({
  origin: ['http://localhost:5173', 'http://127.0.0.1:5173'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging - add BEFORE routes
app.use((req, res, next) => {
  console.log(`📍 ${new Date().toISOString()} - ${req.method} ${req.path}`);
  console.log('Body:', req.body);
  next();
});

// MongoDB connection (optional)
if (process.env.MONGODB_URI) {
  mongoose.connect(process.env.MONGODB_URI)
    .then(() => console.log('✅ MongoDB connected'))
    .catch(err => console.log('⚠️  MongoDB connection optional:', err.message));
} else {
  console.log('⚠️  MongoDB URI not provided. Running without database.');
}

// Health check - BEFORE routes
app.get('/health', (req, res) => {
  res.json({
    status: 'success',
    message: 'StudyMate Backend is running',
    timestamp: new Date().toISOString()
  });
});

// Routes - Make sure this comes AFTER middleware
app.use('/api/chat', chatRoutes);

// Debug logging middleware
app.use((req, res, next) => {
  console.log(`📍 ${req.method} ${req.path}`);
  next();
});

// Test all routes
app.get('/api/test', (req, res) => {
  res.json({
    status: 'success',
    message: 'API is working',
    availableRoutes: [
      'GET /health',
      'GET /api/test',
      'GET /api/chat/test',
      'POST /api/chat/message'
    ]
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    status: 'error',
    message: err.message || 'Internal server error'
  });
});

// 404 handler - should be LAST
app.use((req, res) => {
  console.log(`❌ 404 - Route not found: ${req.method} ${req.path}`);
  res.status(404).json({
    status: 'error',
    message: `Route not found: ${req.method} ${req.path}`,
    availableRoutes: [
      'GET /health',
      'GET /api/test', 
      'GET /api/chat/test',
      'POST /api/chat/message'
    ]
  });
});

// Start server
app.listen(PORT, () => {
  console.log('='.repeat(60));
  console.log(`🚀 StudyMate Backend running on http://localhost:${PORT}`);
  console.log(`📡 AI Service URL: ${process.env.AI_SERVICE_URL || 'http://localhost:5000'}`);
  console.log('='.repeat(60));
}).on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`❌ Port ${PORT} is already in use. Please close other applications or use a different port.`);
  } else {
    console.error('❌ Server error:', err.message);
  }
  process.exit(1);
});

export default app;

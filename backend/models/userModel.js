import mongoose from 'mongoose';

const chatHistorySchema = new mongoose.Schema({
  question: {
    type: String,
    required: true,
    trim: true
  },
  answer: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
  sessionId: {
    type: String,
    default: null
  }
}, {
  timestamps: true
});

// Only create model if MongoDB is connected
let ChatHistory = null;

try {
  if (mongoose.connection.readyState !== 0) {
    ChatHistory = mongoose.model('ChatHistory', chatHistorySchema);
  }
} catch (error) {
  console.log('ChatHistory model not created (MongoDB not connected)');
}

export default ChatHistory;

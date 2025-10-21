# StudyMate Backend

Node.js Express API that connects the React frontend with the Python AI service.

## Features
- RESTful API for chat interactions
- Proxy to Python AI service
- Optional MongoDB integration for chat history
- CORS enabled
- Error handling

## Setup

### Install Dependencies
```bash
npm install
```

### Environment Variables
Create `.env` file:
````
# Server configuration
PORT=3000

# AI service configuration
AI_SERVICE_URL=https://api.openai.com

# MongoDB configuration (optional)
MONGODB_URI=mongodb://localhost:27017

# API keys
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Configure environment
Edit `.env` file with your settings

### Start the server
```bash
npm start
```

Development mode with auto-reload:
```bash
npm run dev
```

Server runs on http://localhost:3000

## API Endpoints

- `GET /health` - Health check
- `POST /api/chat/ask` - Send question to AI service
- `GET /api/chat/history/:userId` - Get chat history (optional)

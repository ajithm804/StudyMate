import { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-center mb-8 text-blue-600">
            📚 StudyMate
          </h1>
          <p className="text-center text-gray-600 mb-8">
            Your AI-powered learning companion for NCERT content
          </p>
          <ChatWindow />
        </div>
      </div>
    </div>
  );
}

export default App;

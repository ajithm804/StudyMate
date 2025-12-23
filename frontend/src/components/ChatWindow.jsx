import { useState, useEffect, useRef } from 'react';
import chatApi from '../api/chatApi';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    if (e) e.preventDefault();
    
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    const currentMessage = inputMessage;
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError('');

    try {
      const response = await chatApi.sendMessage(currentMessage, messages);
      console.log('Full response:', response);
      
      let botText = 'No response';
      
      // Extract answer from different possible paths
      if (response?.data?.response?.answer) {
        botText = response.data.response.answer;
      } else if (response?.data?.answer) {
        botText = response.data.answer;
      } else if (response?.answer) {
        botText = response.answer;
      } else if (response?.data?.response) {
        botText = typeof response.data.response === 'string' 
          ? response.data.response 
          : JSON.stringify(response.data.response);
      } else if (typeof response === 'string') {
        botText = response;
      } else {
        botText = JSON.stringify(response);
      }

      const botMessage = {
        id: Date.now() + 1,
        text: botText,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      
    } catch (err) {
      console.error('Chat error:', err);
      setError(err.message || 'Failed to send message');
      
      const errorMessage = {
        id: Date.now() + 1,
        text: `Error: ${err.message || 'Something went wrong'}`,
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 rounded-t-lg">
        <h2 className="text-xl font-semibold">Chat with StudyMate</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p>👋 Hi! Ask me anything about your NCERT textbooks!</p>
            <p className="text-sm mt-2">Try: "What is photosynthesis?"</p>
          </div>
        )}
        
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg p-3 ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-white'
                  : msg.isError
                  ? 'bg-red-100 text-red-800'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 rounded-lg p-3">
              <p className="text-gray-600">Thinking...</p>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className="px-4 py-2 bg-red-50 border-t border-red-200">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSendMessage} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your question..."
            className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim()}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatWindow;

import React, { useState, useRef, useEffect } from 'react';
import api from '../services/api.js';

export default function ChatbotWidget({ isOpen, onClose, projectPlan }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hi! I\'m your AI assistant. How can I help with your project?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [minimized, setMinimized] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.sendMessage(userMsg);
      setMessages(prev => [...prev, { role: 'assistant', content: response.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${err.message}`
      }]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className={`fixed transition-all duration-300 ${
        minimized ? 'bottom-6 right-6 w-64 h-14' : 'bottom-6 right-6 w-96 h-96'
      } bg-white rounded-lg shadow-2xl flex flex-col border border-slate-200 z-50`}
    >
      {/* Header */}
      <div className="bg-blue-600 text-white px-4 py-3 rounded-t-lg flex justify-between items-center flex-shrink-0">
        <div>
          <h3 className="font-semibold text-sm">AI Chat</h3>
          <p className="text-xs text-blue-100">Ask me anything</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setMinimized(!minimized)}
            className="hover:bg-blue-700 p-1 rounded text-lg leading-none"
            title={minimized ? 'Maximize' : 'Minimize'}
          >
            {minimized ? '🔲' : '−'}
          </button>
          <button
            onClick={onClose}
            className="hover:bg-blue-700 p-1 rounded text-lg leading-none"
            title="Close"
          >
            ✕
          </button>
        </div>
      </div>

      {!minimized && (
        <>
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-100 text-slate-900'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-100 px-3 py-2 rounded-lg text-sm text-slate-600">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSend} className="p-3 border-t border-slate-200 flex-shrink-0">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask..."
                className="input-field text-sm flex-1"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading}
                className="btn-primary text-sm px-3"
              >
                Send
              </button>
            </div>
          </form>
        </>
      )}
    </div>
  );
}
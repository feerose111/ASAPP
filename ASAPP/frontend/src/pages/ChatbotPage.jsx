import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api.js';

export default function ChatbotPage({ projectPlan, onBack }) {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [hasContext, setHasContext] = useState(false);
  const messagesEndRef = useRef(null);

  // Initialize greeting based on whether project exists
  useEffect(() => {
    const greeting = hasContext
      ? `You can now ask about your project "${projectName}". How can I help you?`
      : 'Hi, I\'m from ASAPP. How can I help you? Or if you have any queries related to how ASAPP works or what it is, I can guide you.';

    setMessages([{ role: 'assistant', content: greeting }]);
  }, [hasContext]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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
      setHasContext(response.has_context); // Track context status
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

  return (
    <div className="h-screen flex flex-col bg-slate-50">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-blue-900">Project Discussion</h2>
          <p className="text-slate-600 text-sm">
            {hasContext ? 'Ask questions about your plan' : 'Chat mode (no project context)'}
          </p>
        </div>
        <button
          onClick={() => navigate('/result')}
          className="btn-secondary text-sm"
        >
          ← Back
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xl px-4 py-3 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-slate-900 border border-slate-200'
              }`}
            >
              <p className="text-sm md:text-base leading-relaxed">{msg.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 px-4 py-3 rounded-lg text-slate-600 text-sm">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-slate-200 p-6">
        <form onSubmit={handleSend} className="flex gap-3 max-w-2xl">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="input-field flex-1"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="btn-primary px-6 disabled:opacity-50"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
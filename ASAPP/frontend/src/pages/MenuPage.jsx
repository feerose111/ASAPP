import React, { useState } from 'react';
import api from '../services/api.js';
import ChatbotWidget from '../components/ChatbotWidget.jsx';

const DEFAULT_TECH = [
  'Python', 'Django', 'FastAPI', 'Flask',
  'React', 'Next.js', 'Angular', 'Vue',
  'PostgreSQL', 'MySQL', 'MongoDB', 'SQLite',
  'Docker', 'Kubernetes', 'AWS', 'GCP', 'Azure'
];

export default function MenuPage({ onSubmit }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [chatbotOpen, setChatbotOpen] = useState(false);

  const [form, setForm] = useState({
    project_name: '',
    project_type: '',
    duration: '',
    goals: '',
    description: '',
  });

  const [selectedTech, setSelectedTech] = useState([]);
  const [customInput, setCustomInput] = useState('');
  const [selectedDefaults, setSelectedDefaults] = useState([]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleTechToggle = (tech) => {
    setSelectedDefaults(prev =>
      prev.includes(tech) ? prev.filter(t => t !== tech) : [...prev, tech]
    );
  };

  const handleAddCustom = () => {
    if (customInput.trim() && !selectedTech.includes(customInput.trim())) {
      setSelectedTech(prev => [...prev, customInput.trim()]);
      setCustomInput('');
    }
  };

  const removeTech = (tech, isDefault) => {
    if (isDefault) {
      setSelectedDefaults(prev => prev.filter(t => t !== tech));
    } else {
      setSelectedTech(prev => prev.filter(t => t !== tech));
    }
  };

  const currentTech = [...new Set([...selectedDefaults, ...selectedTech])];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!form.project_name.trim() || !form.project_type.trim() || !form.duration.trim()) {
      setError('Please fill required fields');
      return;
    }

    if (currentTech.length === 0) {
      setError('Select at least one technology');
      return;
    }

    setLoading(true);
    try {
      const result = await api.createProject({
        project_name: form.project_name,
        project_type: form.project_type,
        duration: form.duration,
        tech_stack: currentTech.join(', '),
        goals: form.goals,
        description: form.description || 'No description',
      });
      onSubmit(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setForm({
      project_name: '',
      project_type: '',
      duration: '',
      goals: '',
      description: '',
    });
    setSelectedTech([]);
    setSelectedDefaults([]);
    setCustomInput('');
    setError('');
  };

  return (
    <div className="h-screen flex items-center justify-center p-4 bg-slate-50">
      <div className="card w-full max-w-5xl p-6 md:p-8">
        <div className="mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-blue-900">Create Project</h2>
          <p className="text-slate-600 text-sm md:text-base mt-2">Define scope, goals, and tech stack</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* Horizontal Layout - 2 Columns */}
          <div className="grid md:grid-cols-2 gap-6 max-h-[calc(100vh-250px)] overflow-y-auto">
            {/* Left Column - Basic Info */}
            <div className="space-y-4">
              <h3 className="font-semibold text-slate-900">Project Info</h3>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Project Name *
                </label>
                <input
                  type="text"
                  name="project_name"
                  value={form.project_name}
                  onChange={handleInputChange}
                  placeholder="e.g., AI Research Platform"
                  className="input-field text-sm"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Type *
                </label>
                <input
                  type="text"
                  name="project_type"
                  value={form.project_type}
                  onChange={handleInputChange}
                  placeholder="e.g., research, general"
                  className="input-field text-sm"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Duration (weeks) *
                </label>
                <input
                  type="number"
                  name="duration"
                  value={form.duration}
                  onChange={handleInputChange}
                  placeholder="e.g., 12"
                  className="input-field text-sm"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Goals *
                </label>
                <textarea
                  name="goals"
                  value={form.goals}
                  onChange={handleInputChange}
                  placeholder="Main objectives..."
                  className="input-field text-sm resize-none h-20"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Description
                </label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleInputChange}
                  placeholder="Additional details..."
                  className="input-field text-sm resize-none h-16"
                />
              </div>
            </div>

            {/* Right Column - Tech Stack */}
            <div className="space-y-4">
              <h3 className="font-semibold text-slate-900">Tech Stack</h3>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Select Technologies
                </label>
                <div className="grid grid-cols-2 gap-2 mb-3 max-h-48 overflow-y-auto p-2 bg-slate-50 rounded-lg border border-slate-200">
                  {DEFAULT_TECH.map(tech => (
                    <button
                      key={tech}
                      type="button"
                      onClick={() => handleTechToggle(tech)}
                      className={`px-3 py-2 rounded text-sm font-medium transition-all ${
                        selectedDefaults.includes(tech)
                          ? 'bg-blue-600 text-white'
                          : 'bg-white border border-slate-300 text-slate-700 hover:border-blue-600'
                      }`}
                    >
                      {tech}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex gap-2">
                <input
                  type="text"
                  value={customInput}
                  onChange={(e) => setCustomInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAddCustom()}
                  placeholder="Add custom..."
                  className="input-field text-sm flex-1"
                />
                <button
                  type="button"
                  onClick={handleAddCustom}
                  className="btn-secondary text-sm"
                >
                  Add
                </button>
              </div>

              {currentTech.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Selected ({currentTech.length})
                  </label>
                  <div className="flex flex-wrap gap-2 p-2 bg-slate-50 rounded-lg border border-slate-200 max-h-32 overflow-y-auto">
                    {currentTech.map((tech, idx) => (
                      <div
                        key={`${tech}-${idx}`}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm flex items-center gap-2"
                      >
                        <span>{tech}</span>
                        <button
                          type="button"
                          onClick={() => removeTech(tech, selectedDefaults.includes(tech))}
                          className="hover:text-blue-200 text-lg leading-none"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex gap-3 pt-4 border-t border-slate-200">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex-1 disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Project'}
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="btn-secondary flex-1"
            >
              Reset
            </button>
          </div>
        </form>
      </div>

      {/* Floating Chatbot Button */}
      <button
        onClick={() => setChatbotOpen(!chatbotOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-all flex items-center justify-center text-xl z-40"
        title="Open AI Chat"
      >
        💬
      </button>

      {/* Chatbot Widget */}
      {chatbotOpen && (
        <ChatbotWidget
          isOpen={chatbotOpen}
          onClose={() => setChatbotOpen(false)}
          projectPlan={null}
        />
      )}
    </div>
  );
}
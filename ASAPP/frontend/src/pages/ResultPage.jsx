import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function ResultPage({ apiResult, onReset }) {
  const navigate = useNavigate();

  const handleChat = () => {
    navigate('/chat');
  };

  const handleNewProject = () => {
    onReset();
    navigate('/');
  };

  const renderPlan = (content) => {
    if (!content) return <p className="text-slate-600">No plan available</p>;

    return (
      <div className="prose prose-sm max-w-none">
        {content.split('\n').map((line, idx) => {
          if (line.startsWith('##')) {
            return (
              <h3 key={idx} className="text-lg font-semibold text-blue-700 mt-4 mb-2">
                {line.replace('##', '').trim()}
              </h3>
            );
          }
          if (line.startsWith('#')) {
            return (
              <h2 key={idx} className="text-xl font-bold text-blue-900 mt-6 mb-3">
                {line.replace('#', '').trim()}
              </h2>
            );
          }
          if (line.startsWith('-') || line.startsWith('*')) {
            return (
              <li key={idx} className="ml-4 text-slate-700">
                {line.substring(1).trim()}
              </li>
            );
          }
          if (line.trim()) {
            return (
              <p key={idx} className="text-slate-700 mb-2">
                {line}
              </p>
            );
          }
          return null;
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-full mb-4">
            <span className="text-2xl">✓</span>
          </div>
          <h1 className="text-3xl font-bold text-blue-900 mb-2">Project Plan Ready</h1>
          <p className="text-slate-600">Your research project plan has been generated</p>
        </div>

        {/* Content */}
        <div className="card p-8 mb-8">
          {apiResult.error ? (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              <p className="font-semibold">Error</p>
              <p className="text-sm mt-1">{apiResult.error}</p>
            </div>
          ) : apiResult.project_plan ? (
            <div className="bg-slate-50 p-6 rounded-lg border border-slate-200 max-h-96 overflow-y-auto">
              {renderPlan(apiResult.project_plan)}
            </div>
          ) : (
            <p className="text-slate-600">No plan received</p>
          )}
        </div>

        {/* Actions */}
        <div className="grid md:grid-cols-2 gap-4">
          <button
            onClick={handleChat}
            disabled={!apiResult.project_plan}
            className="btn-primary py-3 disabled:opacity-50"
          >
            💬 Chat About Project
          </button>
          <button
            onClick={handleNewProject}
            className="btn-secondary py-3"
          >
            ➕ Create Another Project
          </button>
        </div>
      </div>
    </div>
  );
}
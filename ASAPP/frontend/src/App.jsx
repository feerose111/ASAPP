import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './index.css';
import MenuPage from './pages/MenuPage.jsx';
import ResultPage from './pages/ResultPage.jsx';
import ChatbotPage from './pages/ChatbotPage.jsx';

function AppContent() {
  const [apiResult, setApiResult] = useState(null);
  const navigate = useNavigate();

  const handleProjectSubmit = (result) => {
    setApiResult(result);
    navigate('/result');
  };

  const handleReset = () => {
    setApiResult(null);
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-900 to-blue-700 text-white py-6 shadow-md">
        <div className="max-w-7xl mx-auto px-4">
          <h1 className="text-2xl md:text-3xl">ASAPP</h1>
          <p className="text-blue-100 text-sm md:text-base">Research Project Planning</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<MenuPage onSubmit={handleProjectSubmit} />} />
          <Route
            path="/result"
            element={
              apiResult ? (
                <ResultPage apiResult={apiResult} onReset={handleReset} />
              ) : (
                <div className="min-h-screen flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-slate-600 mb-4">No project found.</p>
                    <button onClick={handleReset} className="btn-primary">
                      Create Project
                    </button>
                  </div>
                </div>
              )
            }
          />
          <Route
            path="/chat"
            element={
              apiResult?.project_plan ? (
                <ChatbotPage projectPlan={apiResult.project_plan} onBack={handleReset} />
              ) : (
                <div className="min-h-screen flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-slate-600 mb-4">No project plan available.</p>
                    <button onClick={handleReset} className="btn-primary">
                      Go Back
                    </button>
                  </div>
                </div>
              )
            }
          />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="bg-blue-900 text-white text-center py-4 text-sm">
        <p>&copy; 2025 ASAPP - Intelligent Research Planning</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
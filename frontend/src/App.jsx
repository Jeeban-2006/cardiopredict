import { useState } from 'react';
import PredictionForm from './components/PredictionForm';
import EnsembleView from './components/EnsembleView';
import PerformanceDashboard from './components/PerformanceDashboard';
import LandingPage from './components/LandingPage';
import Logo from './components/Logo';
import { BarChart3, Zap, Home } from 'lucide-react';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [activeTab, setActiveTab] = useState('predict');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  if (currentPage === 'landing') {
    return <LandingPage onNavigate={() => setCurrentPage('dashboard')} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-blue-700/30 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all">
              <Logo size={32} />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
                CardioPredict
              </h1>
              <p className="text-xs text-blue-300">AI-Powered Heart Disease Prediction</p>
            </div>
          </div>
          <button
            onClick={() => setCurrentPage('landing')}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 hover:bg-slate-700/50 rounded-lg text-slate-300 transition-all"
          >
            <Home size={18} />
            Home
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-6 mt-8">
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('predict')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'predict'
                ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50'
            }`}
          >
            <Zap size={20} />
            Single Prediction
          </button>
          <button
            onClick={() => setActiveTab('ensemble')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'ensemble'
                ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50'
            }`}
          >
            <Zap size={20} />
            Ensemble Voting
          </button>
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'dashboard'
                ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50'
            }`}
          >
            <BarChart3 size={20} />
            Performance
          </button>
        </div>

        {/* Content */}
        <div className="mb-12">
          {activeTab === 'predict' && (
            <PredictionForm result={result} setResult={setResult} loading={loading} setLoading={setLoading} />
          )}
          {activeTab === 'ensemble' && (
            <EnsembleView result={result} setResult={setResult} loading={loading} setLoading={setLoading} />
          )}
          {activeTab === 'dashboard' && <PerformanceDashboard />}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-blue-700/30 bg-slate-900/80 mt-20 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-slate-400 text-sm">
          <p>
            CardioPredict • Advanced ML Ensemble Model for Heart Disease Detection
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

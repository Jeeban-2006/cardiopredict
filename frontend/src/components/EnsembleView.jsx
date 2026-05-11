import { useState } from 'react';
import axios from 'axios';
import { Zap, AlertCircle } from 'lucide-react';
import FeatureInput from './FeatureInput';
import EnsembleResult from './EnsembleResult';

const FEATURE_NAMES = [
  'Age (years)',
  'Sex (0=F, 1=M)',
  'Chest Pain Type',
  'Resting BP (mmHg)',
  'Serum Cholesterol',
  'Fasting Blood Sugar',
  'ECG Results',
  'Max Heart Rate',
  'Exercise Angina',
  'ST Depression',
  'ST Slope',
  'Major Vessels',
  'Thalassemia'
];

export default function EnsembleView({ result, setResult, loading, setLoading }) {
  const [features, setFeatures] = useState(Array(13).fill(''));
  const [error, setError] = useState('');

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

  const handlePredict = async () => {
    if (features.some(f => f === '')) {
      setError('Please fill in all 13 features');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const numericFeatures = features.map(f => parseFloat(f));
      const response = await axios.post('/api/predict/ensemble', {
        features: numericFeatures
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Ensemble prediction failed');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid lg:grid-cols-2 gap-8">
      {/* Form */}
      <div className="card card-hover">
        <h2 className="text-2xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
          Ensemble Voting System
        </h2>
        <p className="text-sm text-slate-300 mb-6">
          Compare all 5 models simultaneously and get a consensus prediction
        </p>

        <div className="mb-6">
          <label className="block text-sm font-semibold text-purple-300 mb-3">
            Enter 13 Clinical Features
          </label>
          <div className="grid grid-cols-2 gap-3 max-h-72 overflow-y-auto pr-2">
            {features.map((value, idx) => (
              <FeatureInput
                key={idx}
                label={FEATURE_NAMES[idx]}
                value={value}
                onChange={(val) => handleFeatureChange(idx, val)}
              />
            ))}
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center gap-2 text-red-200">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        <button
          onClick={handlePredict}
          disabled={loading}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
        >
          <Zap size={20} />
          {loading ? 'Ensemble Predicting...' : 'Run Ensemble'}
        </button>
      </div>

      {/* Result */}
      {result && <EnsembleResult result={result} />}
      {!result && !loading && (
        <div className="card flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="text-purple-400" size={32} />
            </div>
            <p className="text-slate-400">
              Run ensemble voting for consensus prediction
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

import { useState } from 'react';
import api from '../api';
import ResultCard from './ResultCard';
import FeatureInput from './FeatureInput';
import { Send, AlertCircle } from 'lucide-react';

const MODELS = ['Logistic Regression', 'Random Forest', 'KNN', 'SVM', 'XGBoost'];

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

export default function PredictionForm({ result, setResult, loading, setLoading }) {
  const [selectedModel, setSelectedModel] = useState('Random Forest');
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
      const response = await api.post('/api/predict', {
        features: numericFeatures,
        model: selectedModel
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Prediction failed');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid md:grid-cols-2 gap-8">
      {/* Form */}
      <div className="card card-hover">
        <h2 className="text-2xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
          Patient Information
        </h2>

        {/* Model Selection */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-blue-300 mb-3">
            Select Model
          </label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="input-field bg-slate-700/50"
          >
            {MODELS.map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>
        </div>

        {/* Features Grid */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-blue-300 mb-3">
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

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center gap-2 text-red-200">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {/* Predict Button */}
        <button
          onClick={handlePredict}
          disabled={loading}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <Send size={20} />
          {loading ? 'Predicting...' : 'Get Prediction'}
        </button>
      </div>

      {/* Result */}
      {result && (
        <ResultCard result={result} />
      )}
      {!result && !loading && (
        <div className="card flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Send className="text-blue-400" size={32} />
            </div>
            <p className="text-slate-400">
              Fill in patient data and click predict
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

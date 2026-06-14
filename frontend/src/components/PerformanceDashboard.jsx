import { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart3, TrendingUp } from 'lucide-react';
const API_URL = import.meta.env.VITE_API_URL;

export default function PerformanceDashboard() {
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPerformance = async () => {
      try {
        const response = await axios.get(
          `${API_URL}/api/models/performance`
        );

        setPerformance(response.data);   // <-- MISSING
      } catch (err) {
        console.error('Failed to fetch performance data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPerformance();
  }, []);

  if (loading) {
    return <div className="card text-center py-12 text-slate-400">Loading performance data...</div>;
  }
  if (!performance) {
    return (
      <div className="card text-center py-12 text-red-400">
        Failed to load performance data
      </div>
    );
  }

  const metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc'];
  const metricLabels = {
    accuracy: 'Accuracy',
    precision: 'Precision',
    recall: 'Recall',
    f1: 'F1-Score',
    roc_auc: 'ROC-AUC'
  };

  return (
    <div className="space-y-8">
      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-gradient-to-br from-green-400 to-emerald-400 rounded-lg">
            <BarChart3 className="text-slate-900" size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-400">
              Model Performance Metrics
            </h2>
            <p className="text-sm text-slate-400">Comparison of all 5 trained models</p>
          </div>
        </div>

        {/* Metrics Table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-blue-700/30">
                <th className="text-left py-3 px-4 text-slate-300 font-semibold">Model</th>
                {metrics.map(m => (
                  <th key={m} className="text-center py-3 px-4 text-slate-300 font-semibold">
                    {metricLabels[m]}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Object.entries(performance || {}).map(([model, scores]) => (
                <tr key={model} className="border-b border-blue-700/20 hover:bg-blue-700/10 transition-colors">
                  <td className="py-4 px-4 font-medium text-blue-300">{model}</td>
                  {metrics.map(m => (
                    <td key={m} className="text-center py-4 px-4">
                      <div className="flex items-center justify-center gap-2">
                        <div className="text-white font-semibold">
                          {(scores[m] * 100).toFixed(2)}%
                        </div>
                        <div className="w-24 h-2 bg-slate-700/50 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-cyan-400 to-blue-500"
                            style={{ width: `${scores[m] * 100}%` }}
                          />
                        </div>
                      </div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Key Insights */}
      <div className="grid md:grid-cols-3 gap-4">
        {[
          { label: 'Best Accuracy', value: 'Random Forest & KNN', color: 'from-blue-500 to-cyan-500' },
          { label: 'Highest Recall', value: 'KNN (100%)', color: 'from-green-500 to-emerald-500' },
          { label: 'Best ROC-AUC', value: 'LR & RF (0.95)', color: 'from-purple-500 to-pink-500' }
        ].map((insight, idx) => (
          <div key={idx} className="card border-2 border-slate-700/50">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp size={16} className="text-yellow-400" />
              <p className="text-sm text-slate-400">{insight.label}</p>
            </div>
            <p className={`text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${insight.color}`}>
              {insight.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

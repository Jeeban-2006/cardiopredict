import { CheckCircle, AlertCircle, Users, Vote } from 'lucide-react';

export default function EnsembleResult({ result }) {
  const isDiseasePresent = result.consensus_prediction === 1;
  const votesFor = result.votes_disease;
  const votesAgainst = result.votes_no_disease;

  const models = Object.entries(result.individual_results).map(([name, data]) => ({
    name,
    ...data
  }));

  return (
    <div className="card card-hover">
      <div className="flex items-start justify-between mb-6">
        <h3 className="text-2xl font-bold text-white">Ensemble Consensus</h3>
        <div className={`p-3 rounded-full ${isDiseasePresent ? 'bg-red-500/20' : 'bg-green-500/20'}`}>
          {isDiseasePresent ? (
            <AlertCircle className="text-red-400" size={28} />
          ) : (
            <CheckCircle className="text-green-400" size={28} />
          )}
        </div>
      </div>

      {/* Main Prediction */}
      <div className={`mb-6 p-4 rounded-lg border-2 ${
        isDiseasePresent
          ? 'border-red-500/50 bg-red-500/10'
          : 'border-green-500/50 bg-green-500/10'
      }`}>
        <div className={`text-3xl font-bold ${isDiseasePresent ? 'text-red-400' : 'text-green-400'}`}>
          {result.consensus_label}
        </div>
        <p className="text-sm text-slate-400 mt-1">Consensus Decision</p>
      </div>

      {/* Voting Results */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Vote size={18} className="text-purple-400" />
          <p className="text-sm font-semibold text-purple-300">Model Votes</p>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
            <p className="text-2xl font-bold text-red-400">{votesFor}</p>
            <p className="text-xs text-red-300">Votes for Disease</p>
          </div>
          <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
            <p className="text-2xl font-bold text-green-400">{votesAgainst}</p>
            <p className="text-xs text-green-300">Votes Against</p>
          </div>
        </div>
      </div>

      {/* Confidence */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <label className="text-sm font-semibold text-blue-300">Average Confidence</label>
          <span className="text-lg font-bold text-cyan-400">{result.average_confidence.toFixed(1)}%</span>
        </div>
        <div className="w-full h-3 bg-slate-700/50 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-purple-400 to-pink-400 rounded-full"
            style={{ width: `${result.average_confidence}%` }}
          />
        </div>
      </div>

      {/* Individual Model Results */}
      <div className="pt-4 border-t border-blue-700/30">
        <div className="flex items-center gap-2 mb-3">
          <Users size={18} className="text-cyan-400" />
          <p className="text-sm font-semibold text-cyan-300">Individual Predictions</p>
        </div>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {models.map((model) => (
            <div key={model.name} className="flex items-center justify-between p-2 bg-slate-700/20 rounded-lg">
              <span className="text-sm text-slate-300">{model.name}</span>
              <div className="flex items-center gap-2">
                <span className={`text-sm font-semibold ${
                  model.prediction === 1 ? 'text-red-400' : 'text-green-400'
                }`}>
                  {model.prediction === 1 ? 'Disease' : 'No Disease'}
                </span>
                <div className="w-12 h-2 bg-slate-600 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-400 to-blue-500"
                    style={{ width: `${model.probability_disease * 100}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

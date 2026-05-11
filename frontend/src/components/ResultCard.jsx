import { CheckCircle, AlertCircle } from 'lucide-react';

export default function ResultCard({ result }) {
  const isDiseasePresent = result.prediction === 1;
  const confidence = result.confidence;

  return (
    <div className="card card-hover animate-scale-in">
      <div className="flex items-start justify-between mb-6">
        <h3 className="text-2xl font-bold text-white hover:text-cyan-300 transition-colors">Prediction Result</h3>
        <div className={`p-3 rounded-full transition-all hover:scale-110 ${isDiseasePresent ? 'bg-red-500/20 hover:bg-red-500/40' : 'bg-green-500/20 hover:bg-green-500/40'}`}>
          {isDiseasePresent ? (
            <AlertCircle className="text-red-400 animate-pulse" size={28} />
          ) : (
            <CheckCircle className="text-green-400 animate-bounce" size={28} />
          )}
        </div>
      </div>

      {/* Main Prediction */}
      <div className={`mb-6 p-4 rounded-lg border-2 transition-all hover:shadow-lg ${isDiseasePresent ? 'border-red-500/50 bg-red-500/10 hover:bg-red-500/20 hover:border-red-500/70' : 'border-green-500/50 bg-green-500/10 hover:bg-green-500/20 hover:border-green-500/70'}`}>
        <div className={`text-3xl font-bold ${isDiseasePresent ? 'text-red-400' : 'text-green-400'} hover:scale-110 transition-transform`}>
          {result.label}
        </div>
        <p className="text-sm text-slate-400 mt-1 hover:text-slate-300 transition-colors">Model: {result.model}</p>
      </div>

      {/* Confidence Bar */}
      <div className="mb-6 hover:shadow-lg hover:shadow-cyan-500/20 p-3 rounded-lg transition-all">
        <div className="flex justify-between items-center mb-2">
          <label className="text-sm font-semibold text-blue-300 hover:text-blue-200 transition-colors">Confidence Level</label>
          <span className="text-lg font-bold text-cyan-400 hover:scale-110 transition-transform">{confidence.toFixed(1)}%</span>
        </div>
        <div className="w-full h-3 bg-slate-700/50 rounded-full overflow-hidden hover:shadow-lg hover:shadow-cyan-500/30 transition-all">
          <div
            className={`h-full transition-all rounded-full hover:shadow-inner ${
              confidence > 80 ? 'bg-gradient-to-r from-green-400 to-emerald-400' : confidence > 60 ? 'bg-gradient-to-r from-yellow-400 to-orange-400' : 'bg-gradient-to-r from-orange-400 to-red-400'
            }`}
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      {/* Probability Details */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-3 bg-slate-700/30 rounded-lg border border-blue-700/20 card-hover hover:border-blue-500/50 hover:bg-slate-700/50 hover:shadow-lg hover:shadow-blue-500/20">
          <p className="text-xs text-slate-400 mb-1 hover:text-slate-300 transition-colors">No Disease Probability</p>
          <p className="text-xl font-bold text-blue-300 hover:scale-110 transition-transform">
            {(result.probability_no_disease * 100).toFixed(2)}%
          </p>
        </div>
        <div className="p-3 bg-slate-700/30 rounded-lg border border-blue-700/20 card-hover hover:border-red-500/50 hover:bg-slate-700/50 hover:shadow-lg hover:shadow-red-500/20">
          <p className="text-xs text-slate-400 mb-1 hover:text-slate-300 transition-colors">Disease Probability</p>
          <p className="text-xl font-bold text-red-300 hover:scale-110 transition-transform">
            {(result.probability_disease * 100).toFixed(2)}%
          </p>
        </div>
      </div>

      {/* Model Performance */}
      {result.performance && (
        <div className="pt-4 border-t border-blue-700/30 hover:border-blue-500/50 transition-colors">
          <p className="text-xs text-slate-400 mb-3 font-semibold hover:text-slate-300 transition-colors">Model Performance</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {Object.entries(result.performance).slice(0, 4).map(([key, value]) => (
              <div key={key} className="flex justify-between text-slate-300 hover:text-slate-100 p-1 rounded hover:bg-slate-700/30 transition-all">
                <span className="capitalize text-slate-400 hover:text-slate-300 transition-colors">{key}:</span>
                <span className="font-semibold text-cyan-300 hover:scale-110 transition-transform origin-right">{(value * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

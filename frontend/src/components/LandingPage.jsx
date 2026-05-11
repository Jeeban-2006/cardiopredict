import { ArrowRight, Activity, Brain, TrendingUp, CheckCircle, Users, Zap } from 'lucide-react';
import Logo from './Logo';

const FEATURES = [
  { icon: Brain, title: "Single Model Prediction", desc: "Choose from 5 trained ML models and get instant predictions" },
  { icon: Users, title: "Ensemble Voting", desc: "All 5 models predict simultaneously and vote for consensus" },
  { icon: TrendingUp, title: "Performance Dashboard", desc: "View detailed metrics and model comparison" }
];

const MODELS = [
  { name: "Logistic Regression", accuracy: "86.89%", roc: "95.13%" },
  { name: "Random Forest", accuracy: "88.52%", roc: "95.13%" },
  { name: "KNN", accuracy: "88.52%", roc: "92.32%" },
  { name: "SVM", accuracy: "85.25%", roc: "94.37%" },
  { name: "XGBoost", accuracy: "85.25%", roc: "91.88%" }
];

const STEPS = [
  { step: "1", title: "Input Patient Data", desc: "Enter 13 clinical features" },
  { step: "2", title: "Run Prediction", desc: "Choose a model or use ensemble" },
  { step: "3", title: "Get Results", desc: "Receive instant prediction" },
  { step: "4", title: "View Metrics", desc: "Check model performance" }
];

export default function LandingPage({ onNavigate }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center px-6 pt-20 pb-20 relative overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>

        <div className="max-w-6xl mx-auto relative z-10">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-8 animate-slide-in-left">
              <div className="inline-block mb-4 animate-bounce-custom">
                <span className="px-4 py-2 bg-blue-500/20 border border-blue-500/50 rounded-full text-blue-300 text-sm font-semibold hover:bg-blue-500/30 transition-all flex items-center gap-2">
                  <Logo size={16} />
                  AI-Powered Medical Diagnosis
                </span>
              </div>
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
                Predict Heart Disease with <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400 animate-gradient">Advanced ML</span>
              </h1>
              <p className="text-xl text-slate-300 mb-6">Accurate, fast, and reliable prediction using ensemble machine learning models.</p>

              <div className="grid grid-cols-3 gap-4">
                {[
                  { value: '5', label: 'ML Models' },
                  { value: '88%', label: 'Accuracy' },
                  { value: '100%', label: 'Uptime' }
                ].map((stat, i) => (
                  <div key={i} className="p-4 bg-slate-800/50 border border-blue-700/30 rounded-lg card-hover stagger-item" style={{ animationDelay: `${0.1 * (i + 1)}s` }}>
                    <div className="text-3xl font-bold text-cyan-400">{stat.value}</div>
                    <div className="text-sm text-slate-400">{stat.label}</div>
                  </div>
                ))}
              </div>

              <button onClick={onNavigate} className="btn-primary inline-flex items-center gap-2 text-lg py-4 px-8 group btn-lift">
                Launch Dashboard
                <ArrowRight size={24} className="group-hover:translate-x-1 transition-transform" />
              </button>
            </div>

            <div className="relative animate-slide-in-right">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 blur-3xl rounded-full animate-pulse-custom"></div>
              <div className="relative bg-gradient-to-br from-blue-900/50 to-cyan-900/50 border border-blue-700/30 rounded-2xl p-8 card-hover">
                <div className="space-y-6">
                  {[
                    { icon: CheckCircle, title: "Real-time Predictions", desc: "Instant results with scores", color: 'text-green-400' },
                    { icon: Brain, title: "Ensemble Voting", desc: "5 models voting consensus", color: 'text-purple-400' },
                    { icon: TrendingUp, title: "Performance Tracked", desc: "View metrics comparison", color: 'text-cyan-400' }
                  ].map((f, i) => {
                    const Icon = f.icon;
                    return (
                      <div key={i} className="flex items-center gap-4 p-4 bg-slate-800/50 rounded-lg border border-blue-700/20 card-hover stagger-item" style={{ animationDelay: `${0.4 + 0.1 * i}s` }}>
                        <Icon className={`${f.color} flex-shrink-0 icon-bounce`} size={28} />
                        <div>
                          <div className="font-semibold text-white">{f.title}</div>
                          <div className="text-sm text-slate-400">{f.desc}</div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-20 px-6 bg-slate-900/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-white mb-12 text-center gradient-text">The Problem We Solve</h2>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="card card-hover animate-fade-in-up">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-red-500/20 rounded-lg icon-rotate">
                  <Activity className="text-red-400" size={28} />
                </div>
                <h3 className="text-2xl font-bold text-white">The Challenge</h3>
              </div>
              <p className="text-slate-300 mb-4">Heart disease detection is challenging due to:</p>
              <ul className="space-y-3">
                {['Complex clinical indicators', 'Limited specialist access', 'Time-consuming analysis', 'Risk of human error'].map((item, i) => (
                  <li key={i} className="flex items-start gap-2 stagger-item" style={{ animationDelay: `${0.2 + i * 0.1}s` }}>
                    <span className="text-red-400 font-bold mt-1">•</span>
                    <span className="text-slate-300">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="card card-hover animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-green-500/20 rounded-lg icon-rotate">
                  <Zap className="text-green-400" size={28} />
                </div>
                <h3 className="text-2xl font-bold text-white">Our Solution</h3>
              </div>
              <p className="text-slate-300 mb-4">CardioPredict revolutionizes detection with:</p>
              <ul className="space-y-3">
                {['Instant predictions', '5 ML models', 'Ensemble voting', 'Accessible to all'].map((item, i) => (
                  <li key={i} className="flex items-start gap-2 stagger-item" style={{ animationDelay: `${0.3 + i * 0.1}s` }}>
                    <CheckCircle className="text-green-400 mt-1 flex-shrink-0" size={20} />
                    <span className="text-slate-300">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-white mb-12 text-center gradient-text">Key Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {FEATURES.map((f, i) => {
              const Icon = f.icon;
              return (
                <div key={i} className="card card-hover text-center stagger-item" style={{ animationDelay: `${0.1 * i}s` }}>
                  <div className="flex justify-center mb-4">
                    <div className="p-4 bg-slate-800/50 rounded-lg border border-blue-700/30 icon-bounce">
                      <Icon className="text-blue-400" size={32} />
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">{f.title}</h3>
                  <p className="text-slate-400">{f.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Models Section */}
      <section className="py-20 px-6 bg-slate-900/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-white mb-12 text-center gradient-text">Our ML Models</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-4">
            {MODELS.map((m, i) => (
              <div key={i} className="card card-hover stagger-item" style={{ animationDelay: `${0.1 * i}s` }}>
                <h4 className="font-bold text-white mb-3">{m.name}</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Accuracy</span>
                    <span className="text-cyan-400 font-semibold">{m.accuracy}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">ROC-AUC</span>
                    <span className="text-green-400 font-semibold">{m.roc}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-white mb-12 text-center gradient-text">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {STEPS.map((s, i) => (
              <div key={i} className="card card-hover stagger-item" style={{ animationDelay: `${0.1 * i}s` }}>
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mb-4 icon-bounce">
                  <span className="text-white font-bold">{s.step}</span>
                </div>
                <h3 className="font-bold text-white mb-2">{s.title}</h3>
                <p className="text-sm text-slate-400">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-blue-900/50 to-cyan-900/50">
        <div className="max-w-4xl mx-auto text-center animate-fade-in-up">
          <h2 className="text-4xl font-bold text-white mb-6">Ready to Predict Heart Disease?</h2>
          <p className="text-xl text-slate-300 mb-8">Access the full dashboard and start making predictions instantly</p>
          <button onClick={onNavigate} className="btn-primary inline-flex items-center gap-2 text-lg py-4 px-8 group btn-lift">
            Go to Dashboard
            <ArrowRight size={24} className="group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-blue-700/30 bg-slate-900/80 py-8 px-6">
        <div className="max-w-6xl mx-auto text-center text-slate-400 text-sm">
          <p>CardioPredict • AI-Powered Heart Disease Prediction System</p>
          <p className="mt-2">Using ensemble machine learning for accurate healthcare diagnosis</p>
        </div>
      </footer>
    </div>
  );
}

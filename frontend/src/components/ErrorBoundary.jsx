import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an exception:", error, errorInfo);
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-6 text-white">
          <div className="max-w-md w-full bg-slate-900/80 border border-red-500/30 rounded-2xl p-8 backdrop-blur-md shadow-2xl text-center space-y-6">
            <div className="w-16 h-16 bg-red-500/20 border border-red-500/50 rounded-full flex items-center justify-center mx-auto text-red-400">
              <AlertTriangle size={36} />
            </div>
            
            <div className="space-y-2">
              <h2 className="text-2xl font-bold text-red-400">Something went wrong</h2>
              <p className="text-slate-300 text-sm">
                An unexpected error occurred in the application view.
              </p>
            </div>

            {this.state.error && (
              <div className="bg-slate-950 p-4 rounded-lg text-left text-xs font-mono text-red-300 max-h-40 overflow-y-auto border border-slate-800">
                {this.state.error.toString()}
              </div>
            )}

            <button
              onClick={this.handleReload}
              className="w-full flex items-center justify-center gap-2 py-3 bg-red-500 hover:bg-red-600 rounded-lg font-semibold text-white shadow-lg shadow-red-500/30 transition-all active:scale-95"
            >
              <RefreshCw size={18} />
              Reload Application
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

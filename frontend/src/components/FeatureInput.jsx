export default function FeatureInput({ label, value, onChange }) {
  return (
    <div className="group feature-input">
      <label className="block text-xs text-slate-400 mb-1 group-hover:text-blue-300 transition-colors font-medium">
        {label}
      </label>
      <input
        type="number"
        step="0.01"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="input-field text-sm group-hover:border-blue-400 group-focus-within:border-cyan-400 group-hover:bg-slate-700/60 transition-all"
        placeholder="0.0"
      />
    </div>
  );
}

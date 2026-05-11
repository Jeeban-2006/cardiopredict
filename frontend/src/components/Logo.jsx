export default function Logo({ size = 32, className = "" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Heart shape with gradient */}
      <defs>
        <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#3b82f6" />
          <stop offset="100%" stopColor="#06b6d4" />
        </linearGradient>
        <linearGradient id="pulseGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#3b82f6" stopOpacity="0" />
          <stop offset="50%" stopColor="#06b6d4" stopOpacity="1" />
          <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
        </linearGradient>
      </defs>

      {/* Heart outline */}
      <path
        d="M50,85 C20,70 10,55 10,42 C10,28 20,18 30,18 C38,18 45,24 50,31 C55,24 62,18 70,18 C80,18 90,28 90,42 C90,55 80,70 50,85 Z"
        fill="url(#heartGradient)"
        opacity="0.9"
      />

      {/* Inner heart for depth */}
      <path
        d="M50,82 C22,68 12,54 12,42 C12,30 21,20 32,20 C39,20 46,25 50,31 C54,25 61,20 68,20 C79,20 88,30 88,42 C88,54 78,68 50,82 Z"
        fill="none"
        stroke="url(#pulseGradient)"
        strokeWidth="1.5"
        opacity="0.6"
      />

      {/* Pulse wave lines */}
      <g opacity="0.7">
        <line x1="15" y1="45" x2="30" y2="45" stroke="url(#heartGradient)" strokeWidth="2" strokeLinecap="round" />
        <polyline
          points="30,45 35,35 40,55 45,40 50,50 55,38 60,55 65,42 70,45"
          fill="none"
          stroke="url(#heartGradient)"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <line x1="70" y1="45" x2="85" y2="45" stroke="url(#heartGradient)" strokeWidth="2" strokeLinecap="round" />
      </g>

      {/* AI circuit nodes */}
      <circle cx="20" cy="25" r="2" fill="#06b6d4" opacity="0.8" />
      <circle cx="80" cy="25" r="2" fill="#06b6d4" opacity="0.8" />
      <circle cx="50" cy="15" r="2" fill="#3b82f6" opacity="0.8" />

      {/* Circuit connections */}
      <line x1="20" y1="25" x2="50" y2="15" stroke="#06b6d4" strokeWidth="1" opacity="0.5" />
      <line x1="80" y1="25" x2="50" y2="15" stroke="#06b6d4" strokeWidth="1" opacity="0.5" />
    </svg>
  );
}

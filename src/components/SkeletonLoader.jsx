export default function SkeletonLoader({ className = '', lines = 3 }) {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="skeleton rounded-lg h-4"
          style={{ width: i === lines - 1 ? '60%' : '100%' }}
        />
      ))}
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="rounded-2xl p-6" style={{ background: 'rgba(11,36,71,0.5)', border: '1px solid rgba(255,255,255,0.06)' }}>
      <div className="skeleton rounded-xl h-12 w-12 mb-4" />
      <div className="skeleton rounded h-5 w-40 mb-2" />
      <div className="skeleton rounded h-3 w-full mb-1" />
      <div className="skeleton rounded h-3 w-3/4" />
    </div>
  );
}

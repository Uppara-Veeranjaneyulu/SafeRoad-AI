import { motion } from 'framer-motion';

function ProgressBar({ value, color }) {
  return (
    <div className="h-1.5 rounded-full bg-[#222426]/10 overflow-hidden">
      <motion.div
        initial={{ width: 0 }}
        whileInView={{ width: `${value}%` }}
        viewport={{ once: true }}
        transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
        className="h-full rounded-full"
        style={{ background: color }}
      />
    </div>
  );
}

export default function ModelCard({ name, metrics, color, description, isHighlighted = false }) {
  const metricItems = [
    { label: 'Accuracy', value: metrics.accuracy },
    { label: 'Precision', value: metrics.precision },
    { label: 'Recall', value: metrics.recall },
    { label: 'F1 Score', value: metrics.f1Score },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -6 }}
      className="relative rounded-2xl p-6 overflow-hidden border bg-[#FAF9F2]"
      style={{
        borderColor: isHighlighted ? '#FAD02C' : 'rgba(34, 36, 38, 0.1)',
        boxShadow: isHighlighted ? '0 8px 32px rgba(250, 208, 44, 0.15)' : '0 4px 24px rgba(0, 0, 0, 0.04)',
      }}
    >
      {isHighlighted && (
        <div className="absolute top-3 right-3 px-2 py-0.5 rounded-full text-xs font-semibold bg-[#FAD02C]/10 text-[#E5BD1A] border border-[#FAD02C]/30">
          Best Model
        </div>
      )}

      {/* Model Name */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-3 h-3 rounded-full" style={{ background: color, boxShadow: `0 0 8px ${color}` }} />
        <h3 className="font-display font-bold text-[#222426] text-xl">{name}</h3>
      </div>

      <p className="text-[#4F504E] text-sm mb-6 leading-relaxed">{description}</p>

      {/* Metrics */}
      <div className="space-y-3 mb-6">
        {metricItems.map(({ label, value }) => (
          <div key={label}>
            <div className="flex justify-between mb-1">
              <span className="text-xs text-[#7E7F81]">{label}</span>
              <span className="text-xs font-semibold text-[#222426]">{value}%</span>
            </div>
            <ProgressBar value={value} color={color} />
          </div>
        ))}
      </div>

      {/* Extra Stats */}
      <div className="grid grid-cols-3 gap-3 pt-4 border-t border-[#222426]/5">
        {[
          { label: 'Inference', value: metrics.inferenceTime },
          { label: 'Loss', value: metrics.loss },
          { label: 'Params', value: metrics.params },
        ].map(({ label, value }) => (
          <div key={label} className="text-center">
            <div className="text-sm font-semibold text-[#222426]">{value}</div>
            <div className="text-xs text-[#7E7F81] mt-0.5">{label}</div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

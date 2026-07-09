import { motion } from 'framer-motion';
import CountUp from '../hooks/useCountUp';

export default function AnalyticsCard({ title, value, unit = '', icon: Icon, color = '#FAD02C', trend, isNumber = true, subtitle }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      whileHover={{ y: -4 }}
      className="stat-card relative overflow-hidden group border border-[#222426]/10 bg-[#FAF9F2] shadow-sm rounded-2xl p-6"
    >
      {/* Background glow */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl pointer-events-none"
        style={{ background: `radial-gradient(circle at top right, ${color}08, transparent 70%)` }}
      />

      <div className="flex items-start justify-between mb-4">
        <div
          className="w-11 h-11 rounded-xl flex items-center justify-center"
          style={{ background: `${color}15`, border: `1px solid ${color}25` }}
        >
          {Icon && <Icon className="text-xl" style={{ color }} />}
        </div>
        {trend && (
          <span
            className="text-xs font-semibold px-2 py-1 rounded-full"
            style={{
              background: trend > 0 ? 'rgba(0,168,67,0.08)' : 'rgba(211,47,47,0.08)',
              color: trend > 0 ? '#00A843' : '#D32F2F',
              border: `1px solid ${trend > 0 ? 'rgba(0,168,67,0.15)' : 'rgba(211,47,47,0.15)'}`,
            }}
          >
            {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        )}
      </div>

      <div className="mb-1">
        {isNumber ? (
          <div className="font-display font-bold text-3xl text-[#222426] flex items-end gap-1">
            <CountUp end={typeof value === 'number' ? value : parseFloat(value)} decimals={typeof value === 'number' && value % 1 !== 0 ? 1 : 0} duration={2} />
            {unit && <span className="text-lg text-[#7E7F81] font-normal mb-0.5">{unit}</span>}
          </div>
        ) : (
          <div className="font-display font-bold text-2xl text-[#222426]">{value}</div>
        )}
      </div>

      <p className="text-sm text-[#4F504E]">{title}</p>
      {subtitle && <p className="text-xs text-[#7E7F81] mt-1">{subtitle}</p>}
    </motion.div>
  );
}

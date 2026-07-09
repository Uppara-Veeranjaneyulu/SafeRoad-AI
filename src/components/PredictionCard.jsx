import { motion } from 'framer-motion';
import {
  MdWarning,
  MdCheckCircle,
  MdError,
  MdSpeed,
  MdTimer,
  MdWbSunny,
  MdDirectionsCar,
  MdTraffic,
  MdLightbulb,
  MdBugReport,
} from 'react-icons/md';

const riskConfig = {
  low: {
    label: 'Low Risk',
    color: '#00A843',
    bg: 'rgba(0,168,67,0.06)',
    border: 'rgba(0,168,67,0.15)',
    icon: MdCheckCircle,
    glow: '0 4px 20px rgba(0,168,67,0.05)',
    gradient: 'from-[#00A843]/5 to-transparent',
  },
  moderate: {
    label: 'Moderate Risk',
    color: '#D49A00',
    bg: 'rgba(212,154,0,0.06)',
    border: 'rgba(212,154,0,0.15)',
    icon: MdWarning,
    glow: '0 4px 20px rgba(212,154,0,0.05)',
    gradient: 'from-[#D49A00]/5 to-transparent',
  },
  high: {
    label: 'High Risk',
    color: '#D32F2F',
    bg: 'rgba(211,47,47,0.06)',
    border: 'rgba(211,47,47,0.15)',
    icon: MdError,
    glow: '0 4px 20px rgba(211,47,47,0.05)',
    gradient: 'from-[#D32F2F]/5 to-transparent',
  },
};

function Pill({ children, color }) {
  return (
    <span
      className="px-2.5 py-1 rounded-lg text-xs font-semibold"
      style={{ background: `${color}10`, color, border: `1px solid ${color}20` }}
    >
      {children}
    </span>
  );
}

export default function PredictionCard({ prediction }) {
  if (!prediction) {
    return (
      <div
        className="rounded-2xl p-6 flex flex-col items-center justify-center text-center h-full min-h-[500px] border border-[#222426]/10 bg-[#FAF9F2] shadow-sm"
      >
        <div className="w-20 h-20 rounded-2xl bg-[#222426]/5 border border-[#222426]/10 flex items-center justify-center mb-4">
          <MdTraffic className="text-4xl text-[#7E7F81]" />
        </div>
        <h3 className="text-[#222426] font-semibold mb-2">No Analysis Yet</h3>
        <p className="text-sm text-[#4F504E]">Upload a road image and click analyze to see AI predictions here.</p>
      </div>
    );
  }

  const cfg = riskConfig[prediction.riskLevel] || riskConfig.high;
  const RiskIcon = cfg.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
      className="rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] shadow-sm overflow-hidden"
      style={{
        boxShadow: cfg.glow,
      }}
    >
      {/* Risk Banner */}
      <div className={`px-6 py-5 bg-gradient-to-r ${cfg.gradient} border-b border-[#222426]/5`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <motion.div
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <RiskIcon className="text-4xl" style={{ color: cfg.color }} />
            </motion.div>
            <div>
              <p className="text-xs text-[#7E7F81] uppercase tracking-wider mb-0.5 font-medium">Risk Classification</p>
              <h2 className="font-display font-bold text-2xl text-[#222426]">{prediction.risk}</h2>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-[#7E7F81] mb-0.5 font-medium">Confidence</p>
            <p className="font-display font-bold text-3xl" style={{ color: cfg.color }}>
              {prediction.confidence}%
            </p>
          </div>
        </div>

        {/* Confidence bar */}
        <div className="mt-4 h-2 rounded-full bg-[#222426]/10 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${prediction.confidence}%` }}
            transition={{ duration: 1.5, ease: 'easeOut', delay: 0.3 }}
            className="h-full rounded-full"
            style={{ background: cfg.color }}
          />
        </div>
      </div>

      <div className="p-6 space-y-5">
        {/* Quick Metrics */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Inference', value: prediction.inferenceTime, icon: MdTimer },
            { label: 'Model', value: prediction.model.replace('EfficientNet', 'EffNet'), icon: MdSpeed },
            { label: 'Traffic', value: prediction.trafficDensity, icon: MdTraffic },
          ].map(({ label, value, icon: Icon }) => (
            <div
              key={label}
              className="rounded-xl p-3 text-center bg-[#FEFEF4] border border-[#222426]/5"
            >
              <Icon className="text-[#E5BD1A] text-lg mx-auto mb-1" />
              <p className="text-[#222426] text-xs font-semibold">{value}</p>
              <p className="text-[#7E7F81] text-xs mt-0.5">{label}</p>
            </div>
          ))}
        </div>

        {/* Scene Info */}
        <div>
          <h4 className="text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mb-2">Scene Context</h4>
          <div className="flex flex-wrap gap-2">
            <Pill color="#E5BD1A">{prediction.weather}</Pill>
            <Pill color="#4F504E">{prediction.roadType}</Pill>
            {prediction.yoloObjects.map(obj => (
              <Pill key={obj.label} color="#7E7F81">{obj.label}: {obj.count}</Pill>
            ))}
          </div>
        </div>

        {/* Causes */}
        <div>
          <h4 className="text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <MdBugReport className="text-[#D49A00]" /> Possible Risk Causes
          </h4>
          <ul className="space-y-1.5">
            {prediction.possibleCauses.map((cause, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-[#4F504E]">
                <span className="text-[#D49A00] mt-0.5 shrink-0">•</span>
                {cause}
              </li>
            ))}
          </ul>
        </div>

        {/* Recommendations */}
        <div>
          <h4 className="text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <MdLightbulb className="text-[#00A843]" /> Safety Recommendations
          </h4>
          <ul className="space-y-1.5">
            {prediction.recommendations.map((rec, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.08 }}
                className="flex items-start gap-2 text-sm text-[#4F504E]"
              >
                <span className="text-[#00A843] mt-0.5 shrink-0">✓</span>
                {rec}
              </motion.li>
            ))}
          </ul>
        </div>
      </div>
    </motion.div>
  );
}

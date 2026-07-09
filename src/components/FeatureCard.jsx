import { motion } from 'framer-motion';

export default function FeatureCard({ icon: Icon, title, description, color, index = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ y: -8, scale: 1.01 }}
      className="relative group rounded-2xl p-6 cursor-default overflow-hidden"
      style={{
        background: 'linear-gradient(135deg, rgba(11,36,71,0.7) 0%, rgba(25,55,109,0.3) 100%)',
        border: '1px solid rgba(255,255,255,0.08)',
        boxShadow: '0 4px 24px rgba(0,0,0,0.3)',
      }}
    >
      {/* Hover glow background */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl"
        style={{ background: `radial-gradient(circle at top left, ${color}10 0%, transparent 70%)` }}
      />

      {/* Border glow on hover */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl"
        style={{ border: `1px solid ${color}30` }}
      />

      {/* Icon */}
      <div
        className="relative w-12 h-12 rounded-xl flex items-center justify-center mb-4 transition-transform duration-300 group-hover:scale-110"
        style={{
          background: `${color}15`,
          border: `1px solid ${color}30`,
          boxShadow: `0 0 20px ${color}20`,
        }}
      >
        {Icon && <Icon className="text-2xl" style={{ color }} />}
      </div>

      {/* Content */}
      <h3 className="font-display font-semibold text-white text-lg mb-2 relative">{title}</h3>
      <p className="text-gray-400 text-sm leading-relaxed relative">{description}</p>

      {/* Corner accent */}
      <div
        className="absolute top-0 right-0 w-24 h-24 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{
          background: `radial-gradient(circle at top right, ${color}15, transparent 70%)`,
        }}
      />
    </motion.div>
  );
}

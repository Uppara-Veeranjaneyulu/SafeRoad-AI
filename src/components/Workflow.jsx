import { motion } from 'framer-motion';
import { workflowSteps } from '../data/dummyData';

export default function Workflow() {
  return (
    <div className="flex flex-col items-center">
      {workflowSteps.map((step, index) => (
        <div key={step.id} className="flex flex-col items-center">
          {/* Step Node */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true, margin: '-30px' }}
            transition={{ duration: 0.4, delay: index * 0.08 }}
            whileHover={{ scale: 1.05 }}
            className="relative group"
          >
            <div
              className="flex items-center gap-4 px-6 py-4 rounded-2xl max-w-sm w-full transition-all duration-300"
              style={{
                background: index === 5
                  ? 'linear-gradient(135deg, rgba(0,200,83,0.15) 0%, rgba(11,36,71,0.8) 100%)'
                  : 'linear-gradient(135deg, rgba(11,36,71,0.8) 0%, rgba(25,55,109,0.4) 100%)',
                border: index === 5
                  ? '1px solid rgba(0,200,83,0.3)'
                  : '1px solid rgba(255,255,255,0.08)',
              }}
            >
              {/* Step number */}
              <div className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0 text-lg font-display font-bold"
                style={{
                  background: index === 5 ? 'rgba(0,200,83,0.2)' : 'rgba(255,255,255,0.05)',
                  border: index === 5 ? '1px solid rgba(0,200,83,0.4)' : '1px solid rgba(255,255,255,0.08)',
                  color: index === 5 ? '#00C853' : '#A0AEC0',
                }}>
                {step.icon}
              </div>
              <div>
                <p className="text-white font-semibold text-sm">{step.label}</p>
                <p className="text-gray-400 text-xs mt-0.5">{step.desc}</p>
              </div>

              {/* Step counter badge */}
              <div className="ml-auto w-6 h-6 rounded-full bg-white/5 border border-white/8 flex items-center justify-center text-xs text-gray-500 font-mono shrink-0">
                {step.id}
              </div>
            </div>
          </motion.div>

          {/* Connector Arrow */}
          {index < workflowSteps.length - 1 && (
            <motion.div
              initial={{ opacity: 0, scaleY: 0 }}
              whileInView={{ opacity: 1, scaleY: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.3, delay: index * 0.08 + 0.2 }}
              className="flex flex-col items-center my-1"
              style={{ transformOrigin: 'top' }}
            >
              <div className="w-px h-6 bg-gradient-to-b from-white/15 to-[#00C853]/40" />
              <div className="w-0 h-0"
                style={{
                  borderLeft: '5px solid transparent',
                  borderRight: '5px solid transparent',
                  borderTop: '6px solid rgba(0,200,83,0.4)',
                }}
              />
            </motion.div>
          )}
        </div>
      ))}
    </div>
  );
}

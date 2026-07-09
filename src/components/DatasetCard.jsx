import { motion } from 'framer-motion';
import { MdOpenInNew, MdImage, MdCategory, MdCloud } from 'react-icons/md';

export default function DatasetCard({ dataset, index = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className="rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] shadow-sm overflow-hidden"
    >
      {/* Header */}
      <div className="px-6 py-5 border-b border-[#222426]/5" style={{ background: `${dataset.color}05` }}>
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-2 h-2 rounded-full" style={{ background: dataset.color }} />
              <span className="text-xs font-semibold uppercase tracking-widest" style={{ color: dataset.color }}>{dataset.source}</span>
            </div>
            <h3 className="font-display font-bold text-[#222426] text-2xl">{dataset.name}</h3>
            <p className="text-sm text-[#4F504E] mt-0.5">{dataset.fullName}</p>
          </div>
          <a
            href={dataset.paperUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg transition-all duration-200 hover:scale-105"
            style={{ background: `${dataset.color}10`, color: dataset.color, border: `1px solid ${dataset.color}20` }}
          >
            Paper <MdOpenInNew className="text-xs" />
          </a>
        </div>
      </div>

      <div className="p-6 space-y-5">
        <p className="text-sm text-[#4F504E] leading-relaxed">{dataset.description}</p>

        {/* Key Stats */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Images', value: dataset.totalImages.toLocaleString(), icon: MdImage },
            { label: 'Used', value: dataset.imagesUsed.toLocaleString(), icon: MdCategory },
            { label: 'Resolution', value: dataset.resolution, icon: MdCloud },
          ].map(({ label, value, icon: Icon }) => (
            <div
              key={label}
              className="rounded-xl p-3 text-center bg-[#FEFEF4] border border-[#222426]/5"
            >
              <Icon className="text-lg mx-auto mb-1" style={{ color: dataset.color }} />
              <p className="text-[#222426] text-sm font-semibold">{value}</p>
              <p className="text-[#7E7F81] text-xs mt-0.5">{label}</p>
            </div>
          ))}
        </div>

        {/* Weather Tags */}
        <div>
          <p className="text-xs text-[#7E7F81] uppercase tracking-wider mb-2 font-medium">Weather Conditions</p>
          <div className="flex flex-wrap gap-1.5">
            {dataset.weather.map((w) => (
              <span key={w} className="px-2.5 py-1 rounded-lg text-xs text-[#4F504E] bg-[#FEFEF4] border border-[#222426]/5">{w}</span>
            ))}
          </div>
        </div>

        {/* Road Types */}
        <div>
          <p className="text-xs text-[#7E7F81] uppercase tracking-wider mb-2 font-medium">Road Types</p>
          <div className="flex flex-wrap gap-1.5">
            {dataset.roadTypes.map((r) => (
              <span key={r} className="px-2.5 py-1 rounded-lg text-xs font-medium" style={{ background: `${dataset.color}08`, color: dataset.color, border: `1px solid ${dataset.color}15` }}>{r}</span>
            ))}
          </div>
        </div>

        {/* Class Distribution */}
        <div>
          <p className="text-xs text-[#7E7F81] uppercase tracking-wider mb-3 font-medium">Class Distribution ({dataset.imagesUsed} images used)</p>
          {Object.entries(dataset.classDistribution).map(([cls, count]) => {
            const pct = Math.round((count / dataset.imagesUsed) * 100);
            const color = cls === 'Low Risk' ? '#00A843' : cls === 'Moderate Risk' ? '#D49A00' : '#D32F2F';
            return (
              <div key={cls} className="mb-2">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-[#4F504E]">{cls}</span>
                  <span className="text-[#7E7F81]">{count} ({pct}%)</span>
                </div>
                <div className="h-1.5 rounded-full bg-[#222426]/10 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    whileInView={{ width: `${pct}%` }}
                    viewport={{ once: true }}
                    transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
                    className="h-full rounded-full"
                    style={{ background: color }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Meta */}
        <div className="flex items-center justify-between text-xs text-[#7E7F81] pt-3 border-t border-[#222426]/5">
          <span>Year: {dataset.year}</span>
          <span>{dataset.license}</span>
        </div>
      </div>
    </motion.div>
  );
}

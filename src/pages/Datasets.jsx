import { motion } from 'framer-motion';
import DatasetCard from '../components/DatasetCard';
import { datasets, datasetStats } from '../data/datasetData';

const pipelineSteps = [
  { step: '01', title: 'Data Collection', desc: 'BDD100K + IDD datasets curated for road risk research', color: '#E5BD1A' },
  { step: '02', title: 'Preprocessing', desc: 'Resize → 224×224, Normalize with ImageNet mean/std', color: '#4F504E' },
  { step: '03', title: 'Augmentation', desc: 'Flip, Rotate ±15°, Brightness, Noise, Color Jitter', color: '#7E7F81' },
  { step: '04', title: 'Dataset Split', desc: '80% Train · 10% Validation · 10% Test', color: '#E5BD1A' },
  { step: '05', title: 'Label Encoding', desc: 'Low(0) / Moderate(1) / High(2) risk categories', color: '#4F504E' },
  { step: '06', title: 'TFRecord / DataLoader', desc: 'Optimized tf.data pipeline for GPU training', color: '#7E7F81' },
];

export default function Datasets() {
  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <span className="text-xs font-semibold text-[#E5BD1A] uppercase tracking-widest mb-3 block">Training Data</span>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">Dataset Explorer</h1>
          <p className="text-[#4F504E] max-w-xl mx-auto">
            Two industry-standard datasets combined for robust road safety classification across diverse conditions.
          </p>
          <div className="mt-4 flex items-center justify-center">
            <a
              href="https://ieee-dataport.org/documents/saferoad-ai-multi-source-accident-risk-classification-dataset-0"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-xs font-semibold px-4 py-2.5 rounded-lg text-black bg-[#FAD02C] hover:bg-[#E5BD1A] transition-all duration-300 shadow-sm border border-[#222426]/10"
            >
              Access Dataset on IEEE Dataport
            </a>
          </div>
        </motion.div>

        {/* Combined Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10"
        >
          {[
            { label: 'Total Images Used', value: datasetStats.totalImages.toLocaleString(), color: '#E5BD1A' },
            { label: 'Training Split', value: datasetStats.trainSplit.toLocaleString(), color: '#4F504E' },
            { label: 'Validation Split', value: datasetStats.validationSplit.toLocaleString(), color: '#7E7F81' },
            { label: 'Test Split', value: datasetStats.testSplit.toLocaleString(), color: '#E5BD1A' },
          ].map(({ label, value, color }) => (
            <div key={label} className="rounded-2xl p-5 text-center bg-[#FAF9F2] border border-[#222426]/10 shadow-sm">
              <p className="font-display font-bold text-3xl mb-1" style={{ color }}>{value}</p>
              <p className="text-xs text-[#7E7F81] font-medium">{label}</p>
            </div>
          ))}
        </motion.div>

        {/* Dataset Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          {datasets.map((ds, i) => <DatasetCard key={ds.id} dataset={ds} index={i} />)}
        </div>

        {/* Augmentation Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-6 mb-10 bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
        >
          <h2 className="font-display font-bold text-[#222426] text-xl mb-5">Data Augmentation Techniques</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {datasetStats.augmentations.map((aug) => (
              <div key={aug} className="rounded-xl px-3 py-2.5 text-center text-xs text-[#4F504E] bg-[#FEFEF4] border border-[#222426]/5">{aug}</div>
            ))}
          </div>
        </motion.div>

        {/* Dataset Pipeline */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="font-display font-bold text-[#222426] text-2xl mb-6 text-center">Dataset Processing Pipeline</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {pipelineSteps.map((step, i) => (
              <motion.div
                key={step.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
                className="rounded-2xl p-5 relative overflow-hidden bg-[#FAF9F2] border border-[#222426]/5 hover:border-[#222426]/20 shadow-sm group transition-all duration-300"
              >
                <div className="text-4xl font-display font-bold mb-3 opacity-20" style={{ color: step.color }}>{step.step}</div>
                <h3 className="font-semibold text-[#222426] mb-1">{step.title}</h3>
                <p className="text-sm text-[#4F504E]">{step.desc}</p>
                <div className="absolute top-0 left-0 w-1 h-full rounded-l-2xl" style={{ background: step.color }} />
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

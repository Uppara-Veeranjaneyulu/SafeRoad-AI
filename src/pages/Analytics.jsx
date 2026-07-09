import { motion } from 'framer-motion';
import { MdBubbleChart, MdTimeline } from 'react-icons/md';
import ModelCard from '../components/ModelCard';
import { AccuracyCurveChart, LossCurveChart } from '../components/Charts/AccuracyLossChart';
import { ModelComparisonChart } from '../components/Charts/ModelComparisonChart';
import { modelMetrics } from '../data/dummyData';

function PlaceholderChart({ label, icon: Icon, color }) {
  return (
    <div
      className="rounded-xl flex flex-col items-center justify-center text-center py-16 px-8"
      style={{ background: 'rgba(34, 36, 38, 0.02)', border: '1px dashed rgba(34, 36, 38, 0.1)' }}
    >
      <Icon className="text-4xl mb-3" style={{ color: `${color}60` }} />
      <p className="text-[#4F504E] text-sm font-semibold">{label}</p>
      <p className="text-[#7E7F81] text-xs mt-1">Available after model training</p>
    </div>
  );
}

function SectionCard({ title, subtitle, children }) {
  return (
    <div className="rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] shadow-sm overflow-hidden">
      <div className="px-6 py-4 border-b border-[#222426]/5">
        <h3 className="font-semibold text-[#222426]">{title}</h3>
        {subtitle && <p className="text-xs text-[#7E7F81] mt-0.5">{subtitle}</p>}
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}

export default function Analytics() {
  const models = Object.entries(modelMetrics);

  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <span className="text-xs font-semibold text-[#E5BD1A] uppercase tracking-widest mb-3 block">Model Evaluation</span>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">
            Model Analytics
          </h1>
          <p className="text-[#4F504E] max-w-xl mx-auto">
            Comprehensive performance evaluation of all deep learning models with training curves, confusion matrices, and ROC analysis.
          </p>
        </motion.div>

        {/* Model Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-10">
          {models.map(([name, metrics], i) => (
            <motion.div
              key={name}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
            >
              <ModelCard
                name={name}
                metrics={metrics}
                color={metrics.color}
                description={metrics.description}
                isHighlighted={name === 'EfficientNetB0'}
              />
            </motion.div>
          ))}
        </div>

        {/* Comparison Chart */}
        <div className="mb-6">
          <SectionCard title="Model Performance Comparison" subtitle="Accuracy, Precision, Recall, F1 across all models">
            <div style={{ height: 300 }}>
              <ModelComparisonChart />
            </div>
          </SectionCard>
        </div>

        {/* Training Curves */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
          <SectionCard title="Training Accuracy Curves" subtitle="Model accuracy over 50 epochs">
            <div style={{ height: 280 }}>
              <AccuracyCurveChart />
            </div>
          </SectionCard>
          <SectionCard title="Training Loss Curves" subtitle="Loss reduction over 50 epochs">
            <div style={{ height: 280 }}>
              <LossCurveChart />
            </div>
          </SectionCard>
        </div>

        {/* Placeholder charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-8">
          <SectionCard title="Confusion Matrix" subtitle="EfficientNetB0 · Test Set">
            <PlaceholderChart label="Confusion Matrix" icon={MdBubbleChart} color="#E5BD1A" />
          </SectionCard>
          <SectionCard title="ROC Curve" subtitle="All models · AUC comparison">
            <PlaceholderChart label="ROC Curve" icon={MdTimeline} color="#4F504E" />
          </SectionCard>
          <SectionCard title="Grad-CAM Visualization" subtitle="Feature attribution heatmap">
            <PlaceholderChart label="Grad-CAM Heatmap" icon={MdBubbleChart} color="#7E7F81" />
          </SectionCard>
        </div>

        {/* Metrics Table */}
        <SectionCard title="Detailed Metrics Summary" subtitle="All models compared on test dataset">
          <div className="overflow-x-auto">
            <table className="data-table w-full">
              <thead>
                <tr>
                  <th>Model</th>
                  <th>Accuracy</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1 Score</th>
                  <th>Inference Time</th>
                  <th>Test Loss</th>
                  <th>Parameters</th>
                </tr>
              </thead>
              <tbody>
                {models.map(([name, m]) => (
                  <tr key={name}>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full" style={{ background: m.color }} />
                        <span className="font-semibold text-[#222426] text-sm">{name}</span>
                      </div>
                    </td>
                    <td className="font-semibold" style={{ color: m.color }}>{m.accuracy}%</td>
                    <td className="text-[#4F504E]">{m.precision}%</td>
                    <td className="text-[#4F504E]">{m.recall}%</td>
                    <td className="text-[#4F504E]">{m.f1Score}%</td>
                    <td className="font-mono text-[#00A843] text-xs font-semibold">{m.inferenceTime}</td>
                    <td className="text-[#4F504E]">{m.loss}</td>
                    <td className="text-[#7E7F81] text-xs font-medium">{m.params}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

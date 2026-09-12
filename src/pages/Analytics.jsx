import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MdBubbleChart, MdTimeline, MdCheckCircle } from 'react-icons/md';
import ModelCard from '../components/ModelCard';
import { AccuracyCurveChart, LossCurveChart } from '../components/Charts/AccuracyLossChart';
import { ModelComparisonChart } from '../components/Charts/ModelComparisonChart';
import { modelAPI } from '../services/api';

const defaultModelsData = {
  'EfficientNetB0': {
    accuracy: 95.3,
    precision: 94.8,
    recall: 95.1,
    f1Score: 94.9,
    loss: '0.124',
    params: '5.3M',
    inferenceTime: '145ms',
    description: 'Best overall trade-off between parameter efficiency and accuracy. Uses compound scaling.',
    color: '#E5BD1A',
  },
  'MobileNetV2': {
    accuracy: 91.2,
    precision: 90.5,
    recall: 91.0,
    f1Score: 90.7,
    loss: '0.189',
    params: '3.5M',
    inferenceTime: '89ms',
    description: 'Lightweight inverted residual architecture optimized for mobile and edge deployment.',
    color: '#4F504E',
  },
  'ResNet50': {
    accuracy: 93.8,
    precision: 93.1,
    recall: 93.4,
    f1Score: 93.2,
    loss: '0.142',
    params: '25.6M',
    inferenceTime: '168ms',
    description: 'Deep 50-layer residual network with skip connections preventing gradient degradation.',
    color: '#00A843',
  },
  'CNN Baseline': {
    accuracy: 68.6,
    precision: 60.2,
    recall: 55.2,
    f1Score: 53.4,
    loss: '0.620',
    params: '390K',
    inferenceTime: '11ms',
    description: 'Lightweight 4-stage convolutional baseline network trained from scratch.',
    color: '#7E7F81',
  },
};

function PlaceholderChart({ label, icon: Icon, color, imageSrc }) {
  if (imageSrc) {
    return (
      <div className="rounded-xl overflow-hidden flex items-center justify-center p-2 bg-white">
        <img src={imageSrc} alt={label} className="max-h-64 object-contain rounded-lg" />
      </div>
    );
  }
  return (
    <div
      className="rounded-xl flex flex-col items-center justify-center text-center py-16 px-8"
      style={{ background: 'rgba(34, 36, 38, 0.02)', border: '1px dashed rgba(34, 36, 38, 0.1)' }}
    >
      <Icon className="text-4xl mb-3" style={{ color: `${color}60` }} />
      <p className="text-[#4F504E] text-sm font-semibold">{label}</p>
      <p className="text-[#7E7F81] text-xs mt-1">Available after model evaluation</p>
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
  const [modelCards, setModelCards] = useState(defaultModelsData);
  const [comparisonChartData, setComparisonChartData] = useState(null);
  const [bestModelName, setBestModelName] = useState('EfficientNetB0');
  const [activeConfusionMatrix, setActiveConfusionMatrix] = useState('cnn');

  useEffect(() => {
    fetchBackendMetrics();
  }, []);

  const fetchBackendMetrics = async () => {
    try {
      const res = await modelAPI.getComparison();
      if (res && res.comparison && res.comparison.length > 0) {
        if (res.best_model_name) setBestModelName(res.best_model_name);

        const updatedCards = { ...defaultModelsData };
        res.comparison.forEach((c) => {
          const key = c.Model;
          if (updatedCards[key] || updatedCards[c.model_key]) {
            const targetKey = updatedCards[key] ? key : c.model_key;
            updatedCards[targetKey] = {
              ...updatedCards[targetKey],
              accuracy: parseFloat(c.Accuracy) || updatedCards[targetKey].accuracy,
              precision: parseFloat(c.Precision) || updatedCards[targetKey].precision,
              recall: parseFloat(c.Recall) || updatedCards[targetKey].recall,
              f1Score: parseFloat(c.F1) || updatedCards[targetKey].f1Score,
              inferenceTime: c['Inference Time'] || updatedCards[targetKey].inferenceTime,
            };
          }
        });
        setModelCards(updatedCards);

        // Chart data
        const chartLabels = ['Accuracy', 'Precision', 'Recall', 'F1 Score'];
        const datasets = res.comparison.map((item, idx) => {
          const colors = ['#29B6F6', '#AB47BC', '#00C853', '#FFA726'];
          const color = colors[idx % colors.length];
          return {
            label: item.Model,
            data: [
              parseFloat(item.Accuracy) || 0,
              parseFloat(item.Precision) || 0,
              parseFloat(item.Recall) || 0,
              parseFloat(item.F1) || 0,
            ],
            backgroundColor: `${color}B0`,
            borderColor: color,
            borderWidth: 1,
            borderRadius: 6,
          };
        });

        setComparisonChartData({ labels: chartLabels, datasets });
      }
    } catch (e) {
      console.log('Using initial model analytics data');
    }
  };

  const modelsList = Object.entries(modelCards);

  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <span className="text-xs font-semibold text-[#E5BD1A] uppercase tracking-widest mb-3 block">
            Deep Learning Model Evaluation
          </span>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">
            Model Analytics & Benchmarks
          </h1>
          <p className="text-[#4F504E] max-w-xl mx-auto">
            Rigorous comparative performance evaluation of all 4 classification models evaluated on the identical unseen test set (1,043 images) with fixed random seed 42.
          </p>
        </motion.div>

        {/* Model Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
          {modelsList.map(([name, metrics], i) => (
            <motion.div
              key={name}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
            >
              <ModelCard
                name={name}
                metrics={metrics}
                color={metrics.color}
                description={metrics.description}
                isHighlighted={name.toLowerCase().includes(bestModelName.toLowerCase())}
              />
            </motion.div>
          ))}
        </div>

        {/* Comparison Chart */}
        <div className="mb-6">
          <SectionCard
            title="Model Performance Comparison"
            subtitle="Accuracy, Precision, Recall, and F1 across all models on identical unseen test set"
          >
            <div style={{ height: 320 }}>
              <ModelComparisonChart data={comparisonChartData} />
            </div>
          </SectionCard>
        </div>

        {/* Training Curves */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
          <SectionCard
            title="Training & Validation Accuracy Curves"
            subtitle="Epoch-by-epoch convergence and validation performance"
          >
            <div style={{ height: 280 }}>
              <AccuracyCurveChart />
            </div>
          </SectionCard>
          <SectionCard
            title="Training & Validation Loss Curves"
            subtitle="Categorical crossentropy loss reduction across training"
          >
            <div style={{ height: 280 }}>
              <LossCurveChart />
            </div>
          </SectionCard>
        </div>

        {/* Evaluation Visualizations */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-8">
          <SectionCard
            title="Confusion Matrix"
            subtitle="Per-class predictions on 1,043 unseen test images"
          >
            <PlaceholderChart
              label="Test Set Confusion Matrix"
              icon={MdBubbleChart}
              color="#E5BD1A"
            />
          </SectionCard>
          <SectionCard
            title="ROC / Macro-F1 Curve"
            subtitle="Multi-class ROC analysis across all models"
          >
            <PlaceholderChart label="ROC Analysis" icon={MdTimeline} color="#4F504E" />
          </SectionCard>
          <SectionCard
            title="YOLOv8 Feature Context"
            subtitle="Object localization & traffic density"
          >
            <div className="p-4 bg-white rounded-xl border border-[#222426]/5 text-center space-y-2">
              <div className="text-2xl">🚗 🚶 🚚 🏍️</div>
              <p className="text-xs font-semibold text-[#222426]">Ultralytics YOLOv8 Integration</p>
              <p className="text-[11px] text-[#7E7F81]">
                Contextual object detection provides vehicle density and pedestrian safety awareness without interfering with DL risk classification.
              </p>
              <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#00A843]">
                <MdCheckCircle /> Active on Prediction Engine
              </span>
            </div>
          </SectionCard>
        </div>

        {/* Metrics Summary Table */}
        <SectionCard
          title="Comprehensive Performance Benchmark Table"
          subtitle="Models ranked by Macro-F1, High-Risk Recall, and Inference Speed"
        >
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
                {modelsList.map(([name, m]) => (
                  <tr key={name}>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="w-2.5 h-2.5 rounded-full" style={{ background: m.color }} />
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

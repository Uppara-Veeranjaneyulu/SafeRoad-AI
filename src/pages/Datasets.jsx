import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import DatasetCard from '../components/DatasetCard';
import { datasets as initialDatasets, datasetStats as initialStats } from '../data/datasetData';
import { datasetAPI } from '../services/api';
import { MdCheckCircle, MdSecurity, MdWarning, MdShield } from 'react-icons/md';

const pipelineSteps = [
  { step: '01', title: 'Multi-Source Curation', desc: 'BDD100K + IDD + Custom YouTube intersection captures', color: '#2563EB' },
  { step: '02', title: 'Standardized Preprocessing', desc: 'Read RGB → Bilinear resize to 224×224 → Normalize [0, 1]', color: '#4F504E' },
  { step: '03', title: 'Train-Only Augmentation', desc: 'Horizontal flip, rotation ±10°, zoom ±10%, brightness ±10%', color: '#7E7F81' },
  { step: '04', title: 'Leakage-Free 70/15/15 Split', desc: '4,864 Train · 1,042 Validation · 1,043 Isolated Test (Seed 42)', color: '#2563EB' },
  { step: '05', title: 'Training Class Weighting', desc: 'Inverse-frequency weights calculated strictly on training set', color: '#4F504E' },
  { step: '06', title: 'Decoupled YOLOv8 & DL Evaluation', desc: 'Traffic density estimation + 4 DL models on unseen test set', color: '#7E7F81' },
];

export default function Datasets() {
  const [stats, setStats] = useState(initialStats);
  const [datasetsList, setDatasetsList] = useState(initialDatasets);
  const [isLive, setIsLive] = useState(false);

  useEffect(() => {
    let mounted = true;
    datasetAPI.getStats()
      .then((res) => {
        if (!mounted || !res) return;
        setIsLive(true);
        if (res.totalImages) {
          setStats((prev) => ({
            ...prev,
            totalImages: res.totalImages,
            trainSplit: res.trainSplit || prev.trainSplit,
            validationSplit: res.validationSplit || prev.validationSplit,
            testSplit: res.testSplit || prev.testSplit,
            classDistribution: res.classDistribution || prev.classDistribution,
          }));
        }
      })
      .catch(() => {
        // Smoothly fall back to verified static datasetStats
        setIsLive(false);
      });

    return () => { mounted = false; };
  }, []);

  const classDist = stats.classDistribution || initialStats.classDistribution;

  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-[#2563EB]/10 text-[#2563EB] mb-3">
            <MdCheckCircle className="text-sm" />
            <span>{isLive ? 'Live Backend Connected' : 'Verified Dataset Audit'} · 6,949 Processed Images</span>
          </div>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">Dataset Explorer</h1>
          <p className="text-[#4F504E] max-w-2xl mx-auto text-sm sm:text-base leading-relaxed">
            Multi-source road scene repository aggregating <b>BDD100K</b>, <b>India Driving Dataset (IDD)</b>, and <b>Curated YouTube Intersection Videos</b> with zero data leakage across an isolated 70% / 15% / 15% split.
          </p>
          <div className="mt-5 flex items-center justify-center gap-3">
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

        {/* Combined Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10"
        >
          {[
            { label: 'Total Images Processed', value: stats.totalImages.toLocaleString(), sub: '100% Audited & Valid', color: '#2563EB' },
            { label: 'Training Set (70%)', value: stats.trainSplit.toLocaleString(), sub: 'Class Weighted', color: '#4F504E' },
            { label: 'Validation Set (15%)', value: stats.validationSplit.toLocaleString(), sub: 'Zero Augmentation', color: '#7E7F81' },
            { label: 'Unseen Test Set (15%)', value: stats.testSplit.toLocaleString(), sub: 'Strictly Isolated', color: '#10B981' },
          ].map(({ label, value, sub, color }) => (
            <div key={label} className="rounded-2xl p-5 text-center bg-[#FAF9F2] border border-[#222426]/10 shadow-sm hover:border-[#222426]/20 transition-all">
              <p className="font-display font-bold text-3xl mb-1" style={{ color }}>{value}</p>
              <p className="text-xs text-[#222426] font-semibold">{label}</p>
              <p className="text-[11px] text-[#7E7F81] mt-0.5">{sub}</p>
            </div>
          ))}
        </motion.div>

        {/* Class Distribution Breakdown Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-6 sm:p-7 mb-12 bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6 border-b border-[#222426]/5 pb-4">
            <div>
              <h2 className="font-display font-bold text-[#222426] text-xl">Ground-Truth Class Distribution</h2>
              <p className="text-xs text-[#4F504E] mt-0.5">Exact split counts and training inverse-frequency class weights</p>
            </div>
            <div className="flex items-center gap-2 text-xs font-medium text-[#7E7F81] bg-[#FEFEF4] px-3 py-1.5 rounded-lg border border-[#222426]/5">
              <span>Split Ratio: <b>70% · 15% · 15%</b> (Seed 42)</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Safe */}
            {classDist['Safe'] && (
              <div className="rounded-xl p-4 bg-[#FEFEF4] border border-[#10B981]/20">
                <div className="flex items-center justify-between mb-2">
                  <span className="inline-flex items-center gap-1.5 text-xs font-bold text-[#10B981]">
                    <MdShield className="text-sm" /> Safe (Low Risk)
                  </span>
                  <span className="text-xs font-bold text-[#10B981] bg-[#10B981]/10 px-2 py-0.5 rounded">
                    {classDist['Safe'].percentage}
                  </span>
                </div>
                <div className="text-2xl font-display font-bold text-[#222426] mb-1">
                  {classDist['Safe'].count.toLocaleString()} <span className="text-xs font-normal text-[#7E7F81]">images</span>
                </div>
                <div className="w-full bg-[#222426]/5 h-2 rounded-full overflow-hidden mb-3">
                  <div className="bg-[#10B981] h-full rounded-full" style={{ width: classDist['Safe'].percentage }} />
                </div>
                <div className="grid grid-cols-3 gap-1 text-[11px] text-[#4F504E] border-t border-[#222426]/5 pt-2">
                  <div>Train: <b>{classDist['Safe'].train}</b></div>
                  <div>Val: <b>{classDist['Safe'].val}</b></div>
                  <div>Test: <b>{classDist['Safe'].test}</b></div>
                </div>
                <div className="text-[11px] text-[#7E7F81] mt-2 font-medium">
                  Class Weight: <span className="text-[#222426] font-semibold">{classDist['Safe'].weight}</span>
                </div>
              </div>
            )}

            {/* Moderate Risk */}
            {classDist['Moderate Risk'] && (
              <div className="rounded-xl p-4 bg-[#FEFEF4] border border-[#F59E0B]/20">
                <div className="flex items-center justify-between mb-2">
                  <span className="inline-flex items-center gap-1.5 text-xs font-bold text-[#F59E0B]">
                    <MdWarning className="text-sm" /> Moderate Risk
                  </span>
                  <span className="text-xs font-bold text-[#F59E0B] bg-[#F59E0B]/10 px-2 py-0.5 rounded">
                    {classDist['Moderate Risk'].percentage}
                  </span>
                </div>
                <div className="text-2xl font-display font-bold text-[#222426] mb-1">
                  {classDist['Moderate Risk'].count.toLocaleString()} <span className="text-xs font-normal text-[#7E7F81]">images</span>
                </div>
                <div className="w-full bg-[#222426]/5 h-2 rounded-full overflow-hidden mb-3">
                  <div className="bg-[#F59E0B] h-full rounded-full" style={{ width: classDist['Moderate Risk'].percentage }} />
                </div>
                <div className="grid grid-cols-3 gap-1 text-[11px] text-[#4F504E] border-t border-[#222426]/5 pt-2">
                  <div>Train: <b>{classDist['Moderate Risk'].train}</b></div>
                  <div>Val: <b>{classDist['Moderate Risk'].val}</b></div>
                  <div>Test: <b>{classDist['Moderate Risk'].test}</b></div>
                </div>
                <div className="text-[11px] text-[#7E7F81] mt-2 font-medium">
                  Class Weight: <span className="text-[#222426] font-semibold">{classDist['Moderate Risk'].weight}</span> <span className="text-[#F59E0B]">(High Penalty)</span>
                </div>
              </div>
            )}

            {/* High Risk */}
            {classDist['High Risk'] && (
              <div className="rounded-xl p-4 bg-[#FEFEF4] border border-[#EF4444]/20">
                <div className="flex items-center justify-between mb-2">
                  <span className="inline-flex items-center gap-1.5 text-xs font-bold text-[#EF4444]">
                    <MdSecurity className="text-sm" /> High Risk
                  </span>
                  <span className="text-xs font-bold text-[#EF4444] bg-[#EF4444]/10 px-2 py-0.5 rounded">
                    {classDist['High Risk'].percentage}
                  </span>
                </div>
                <div className="text-2xl font-display font-bold text-[#222426] mb-1">
                  {classDist['High Risk'].count.toLocaleString()} <span className="text-xs font-normal text-[#7E7F81]">images</span>
                </div>
                <div className="w-full bg-[#222426]/5 h-2 rounded-full overflow-hidden mb-3">
                  <div className="bg-[#EF4444] h-full rounded-full" style={{ width: classDist['High Risk'].percentage }} />
                </div>
                <div className="grid grid-cols-3 gap-1 text-[11px] text-[#4F504E] border-t border-[#222426]/5 pt-2">
                  <div>Train: <b>{classDist['High Risk'].train}</b></div>
                  <div>Val: <b>{classDist['High Risk'].val}</b></div>
                  <div>Test: <b>{classDist['High Risk'].test}</b></div>
                </div>
                <div className="text-[11px] text-[#7E7F81] mt-2 font-medium">
                  Class Weight: <span className="text-[#222426] font-semibold">{classDist['High Risk'].weight}</span>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        {/* Dataset Source Cards */}
        <div className="mb-12">
          <div className="text-center mb-8">
            <h2 className="font-display font-bold text-[#222426] text-2xl sm:text-3xl mb-2">Curated Dataset Sources</h2>
            <p className="text-sm text-[#4F504E] max-w-xl mx-auto">Three diverse multi-source repositories combined to train robust deep learning classifiers.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {datasetsList.map((ds, i) => <DatasetCard key={ds.id} dataset={ds} index={i} />)}
          </div>
        </div>

        {/* Augmentation Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-6 sm:p-7 mb-12 bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-5">
            <div>
              <h2 className="font-display font-bold text-[#222426] text-xl">Training Data Augmentations</h2>
              <p className="text-xs text-[#4F504E] mt-0.5">Applied <b>strictly to training images only</b> to prevent test leakage and boost model generalization</p>
            </div>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-[#10B981]/10 text-[#10B981] self-start sm:self-auto">
              Validation & Test: Zero Augmentation
            </span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {stats.augmentations.map((aug) => (
              <div key={aug} className="rounded-xl px-3 py-3 text-center text-xs font-medium text-[#222426] bg-[#FEFEF4] border border-[#222426]/5 shadow-2xs">
                {aug}
              </div>
            ))}
          </div>
        </motion.div>

        {/* Dataset Pipeline */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="font-display font-bold text-[#222426] text-2xl sm:text-3xl mb-2 text-center">Dataset Processing Pipeline</h2>
          <p className="text-sm text-[#4F504E] text-center max-w-lg mx-auto mb-8">End-to-end data engineering protocol guaranteeing reproducible, leakage-free modeling.</p>
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
                <p className="text-sm text-[#4F504E] leading-relaxed">{step.desc}</p>
                <div className="absolute top-0 left-0 w-1 h-full rounded-l-2xl" style={{ background: step.color }} />
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

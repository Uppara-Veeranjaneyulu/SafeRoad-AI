import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MdAutoAwesome } from 'react-icons/md';
import UploadCard from '../components/UploadCard';
import PredictionCard from '../components/PredictionCard';
import { dummyPrediction } from '../data/dummyData';

export default function Prediction() {
  const [image, setImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageSelect = (file, preview) => {
    setImage(file ? preview : null);
    setResult(null);
  };

  // Simulate analysis (no real backend)
  const handleAnalyze = () => {
    if (!image) return;
    setIsAnalyzing(true);
    setResult(null);
    setTimeout(() => {
      setIsAnalyzing(false);
      setResult(dummyPrediction);
    }, 2200);
  };

  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <span className="text-xs font-semibold text-[#E5BD1A] uppercase tracking-widest mb-3 block">AI Prediction Engine</span>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">
            Road Risk Classification
          </h1>
          <p className="text-[#4F504E] max-w-xl mx-auto">
            Upload a road scene image and our deep learning models will analyze and classify the risk level in milliseconds.
          </p>
        </motion.div>

        {/* Main Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Upload */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex flex-col"
          >
            <div onClick={image ? handleAnalyze : undefined}>
              <UploadCard onImageSelect={handleImageSelect} />
            </div>

            {/* Analyze trigger */}
            {image && !isAnalyzing && !result && (
              <motion.button
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={handleAnalyze}
                className="mt-4 w-full py-4 rounded-2xl font-semibold text-sm flex items-center justify-center gap-2 btn-primary"
                id="run-prediction-btn"
              >
                <MdAutoAwesome className="text-lg" />
                Run AI Analysis
              </motion.button>
            )}

            {/* Loading state */}
            <AnimatePresence>
              {isAnalyzing && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="mt-4 rounded-2xl p-6 text-center bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
                >
                  <div className="flex items-center justify-center gap-3 mb-3">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="w-6 h-6 rounded-full border-2 border-[#E5BD1A] border-t-transparent"
                    />
                    <span className="text-[#E5BD1A] font-semibold text-sm">Analyzing road scene...</span>
                  </div>

                  <div className="space-y-2 text-left">
                    {[
                      { label: 'Preprocessing image', delay: 0 },
                      { label: 'Running YOLOv8 detection', delay: 0.4 },
                      { label: 'EfficientNetB0 inference', delay: 0.8 },
                      { label: 'Generating recommendations', delay: 1.2 },
                    ].map((step) => (
                      <motion.div
                        key={step.label}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: step.delay }}
                        className="flex items-center gap-2 text-xs text-[#4F504E]"
                      >
                        <motion.div
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ duration: 0.5, delay: step.delay }}
                          className="w-1.5 h-1.5 rounded-full bg-[#E5BD1A]"
                        />
                        {step.label}
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Sample Images hint */}
            <div className="mt-6 p-4 rounded-xl bg-[#FAF9F2] border border-[#222426]/10">
              <p className="text-xs text-[#7E7F81] mb-2 uppercase tracking-wider font-semibold">Sample test images available in:</p>
              <code className="text-xs text-[#E5BD1A] font-mono">datasets/ → BDD100K, IDD</code>
            </div>
          </motion.div>

          {/* Right: Results */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <PredictionCard prediction={result} />
          </motion.div>
        </div>

        {/* Model Info Strip */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4"
        >
          {[
            { name: 'EfficientNetB0', acc: '95.3%', time: '145ms', color: '#E5BD1A' },
            { name: 'MobileNetV2', acc: '91.2%', time: '89ms', color: '#4F504E' },
            { name: 'CNN Baseline', acc: '88.4%', time: '210ms', color: '#7E7F81' },
          ].map((m) => (
            <div
              key={m.name}
              className="rounded-xl px-5 py-4 flex items-center justify-between bg-[#FAF9F2] border border-[#222426]/10"
            >
              <div>
                <p className="text-sm font-semibold text-[#222426]">{m.name}</p>
                <p className="text-xs text-[#7E7F81] mt-0.5">Deep Learning Model</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold" style={{ color: m.color }}>{m.acc}</p>
                <p className="text-xs text-[#7E7F81]">{m.time} avg</p>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MdAutoAwesome, MdSpeed, MdWarningAmber, MdCheckCircleOutline } from 'react-icons/md';
import UploadCard from '../components/UploadCard';
import PredictionCard from '../components/PredictionCard';
import { predictionAPI, modelAPI, healthAPI } from '../services/api';

export default function Prediction() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedModel, setSelectedModel] = useState('best');
  const [backendOnline, setBackendOnline] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [modelComparison, setModelComparison] = useState([]);
  const [bestModelName, setBestModelName] = useState('Best Model');

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth();
    fetchModelInfo();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await healthAPI.check();
      setBackendOnline(true);
      setErrorMessage(null);
    } catch (err) {
      setBackendOnline(false);
    }
  };

  const fetchModelInfo = async () => {
    try {
      const res = await modelAPI.getComparison();
      if (res && res.comparison) {
        setModelComparison(res.comparison);
        if (res.best_model_name) setBestModelName(res.best_model_name);
      }
    } catch (e) {
      // Backend not yet ready
    }
  };

  const handleImageSelect = (file, preview) => {
    setSelectedFile(file);
    setImagePreview(preview);
    setResult(null);
    setErrorMessage(null);
  };

  // Real backend prediction call
  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);
    setResult(null);
    setErrorMessage(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await predictionAPI.predict(formData, selectedModel);
      setResult(response);
      setBackendOnline(true);
    } catch (error) {
      console.error('Prediction error:', error);
      setBackendOnline(false);
      setErrorMessage(
        error.response?.data?.error ||
        'Backend not connected. Please ensure the Python Flask backend is running on port 5000.'
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <span className="text-xs font-semibold text-[#E5BD1A] uppercase tracking-widest mb-3 block">
            AI Prediction Engine
          </span>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">
            Road Risk Classification
          </h1>
          <p className="text-[#4F504E] max-w-xl mx-auto">
            Upload a road scene image and our deep learning models with YOLOv8 traffic monitoring will analyze and classify the risk level in real time.
          </p>

          {/* Backend Status Indicator */}
          <div className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border bg-[#FAF9F2] border-[#222426]/10">
            {backendOnline === true && (
              <>
                <span className="w-2 h-2 rounded-full bg-[#00A843] animate-pulse" />
                <span className="text-[#00A843]">Backend Connected (Flask API :5000)</span>
              </>
            )}
            {backendOnline === false && (
              <>
                <span className="w-2 h-2 rounded-full bg-[#D32F2F]" />
                <span className="text-[#D32F2F]">Backend Not Connected</span>
                <button
                  onClick={checkBackendHealth}
                  className="ml-2 text-xs underline text-[#7E7F81] hover:text-[#222426]"
                >
                  Retry
                </button>
              </>
            )}
            {backendOnline === null && (
              <>
                <span className="w-2 h-2 rounded-full bg-[#E5BD1A] animate-pulse" />
                <span className="text-[#7E7F81]">Checking backend connection...</span>
              </>
            )}
          </div>
        </motion.div>

        {/* Backend offline alert if analyze attempted and failed */}
        {errorMessage && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 rounded-xl bg-[#D32F2F]/10 border border-[#D32F2F]/30 text-[#D32F2F] flex items-center gap-3 text-sm"
          >
            <MdWarningAmber className="text-xl shrink-0" />
            <div>
              <p className="font-semibold">Backend Communication Error</p>
              <p className="text-xs mt-0.5 opacity-90">{errorMessage}</p>
            </div>
          </motion.div>
        )}

        {/* Main Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Upload and Controls */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex flex-col"
          >
            <UploadCard onImageSelect={handleImageSelect} />

            {/* Model Selector Card */}
            <div className="mt-4 p-4 rounded-xl bg-[#FAF9F2] border border-[#222426]/10">
              <label htmlFor="model-select" className="flex items-center justify-between text-xs font-semibold text-[#4F504E] uppercase tracking-wider mb-2">
                <span className="flex items-center gap-1.5">
                  <MdSpeed className="text-[#E5BD1A] text-base" />
                  Select Classification Model:
                </span>
                <span className="text-[#E5BD1A] font-bold lowercase font-mono">
                  {selectedModel === 'best' ? `auto (${bestModelName})` : selectedModel}
                </span>
              </label>
              <select
                id="model-select"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="w-full bg-[#FEFEF4] border border-[#222426]/20 rounded-lg px-3 py-2 text-sm text-[#222426] focus:outline-none focus:border-[#E5BD1A] font-medium"
              >
                <option value="best">⭐ Best Model (Auto-selected by Macro-F1)</option>
                <option value="cnn">Custom CNN Baseline</option>
                <option value="mobilenetv2">MobileNetV2 (Pretrained Transfer)</option>
                <option value="efficientnetb0">EfficientNetB0 (Pretrained Transfer)</option>
                <option value="resnet50">ResNet50 (Pretrained Transfer)</option>
              </select>
              <p className="text-[11px] text-[#7E7F81] mt-1.5">
                YOLOv8 simultaneously analyzes traffic density, vehicle counts, and pedestrians in all selections.
              </p>
            </div>

            {/* Analyze trigger */}
            {imagePreview && !isAnalyzing && (
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
                    <span className="text-[#E5BD1A] font-semibold text-sm">
                      Executing Real AI Inference...
                    </span>
                  </div>

                  <div className="space-y-2 text-left">
                    {[
                      { label: 'Preprocessing 224x224 RGB image', delay: 0 },
                      { label: 'Running Ultralytics YOLOv8 traffic & object detection', delay: 0.3 },
                      { label: `Executing ${selectedModel === 'best' ? bestModelName : selectedModel} deep learning inference`, delay: 0.6 },
                      { label: 'Generating context-aware risk recommendations', delay: 0.9 },
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
              <p className="text-xs text-[#7E7F81] mb-1 uppercase tracking-wider font-semibold">
                Trained Dataset Categories:
              </p>
              <p className="text-xs text-[#4F504E]">
                BDD100K · India Driving Dataset (IDD) · YouTube Intersections (6,949 images total)
              </p>
            </div>
          </motion.div>

          {/* Right: Real Prediction Results */}
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
          className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          {[
            {
              name: 'EfficientNetB0',
              acc: modelComparison.find((m) => m.model_key === 'efficientnetb0')?.Accuracy || 'Trained',
              time: modelComparison.find((m) => m.model_key === 'efficientnetb0')?.['Inference Time'] || 'DL Model',
              color: '#E5BD1A',
            },
            {
              name: 'MobileNetV2',
              acc: modelComparison.find((m) => m.model_key === 'mobilenetv2')?.Accuracy || 'Trained',
              time: modelComparison.find((m) => m.model_key === 'mobilenetv2')?.['Inference Time'] || 'DL Model',
              color: '#4F504E',
            },
            {
              name: 'ResNet50',
              acc: modelComparison.find((m) => m.model_key === 'resnet50')?.Accuracy || 'Trained',
              time: modelComparison.find((m) => m.model_key === 'resnet50')?.['Inference Time'] || 'DL Model',
              color: '#00A843',
            },
            {
              name: 'Custom CNN',
              acc: modelComparison.find((m) => m.model_key === 'cnn')?.Accuracy || 'Trained',
              time: modelComparison.find((m) => m.model_key === 'cnn')?.['Inference Time'] || 'Baseline',
              color: '#7E7F81',
            },
          ].map((m) => (
            <div
              key={m.name}
              className="rounded-xl px-4 py-3 flex items-center justify-between bg-[#FAF9F2] border border-[#222426]/10"
            >
              <div>
                <p className="text-sm font-semibold text-[#222426]">{m.name}</p>
                <p className="text-xs text-[#7E7F81] mt-0.5">Classification Engine</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold" style={{ color: m.color }}>{m.acc}</p>
                <p className="text-xs text-[#7E7F81]">{m.time}</p>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}

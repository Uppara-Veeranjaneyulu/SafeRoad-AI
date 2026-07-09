import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MdCloudUpload, MdImage, MdClose, MdPhotoCamera } from 'react-icons/md';

export default function UploadCard({ onImageSelect }) {
  const [dragOver, setDragOver] = useState(false);
  const [preview, setPreview] = useState(null);
  const [fileName, setFileName] = useState('');

  const handleFile = useCallback((file) => {
    if (!file || !file.type.startsWith('image/')) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target.result);
      if (onImageSelect) onImageSelect(file, e.target.result);
    };
    reader.readAsDataURL(file);
  }, [onImageSelect]);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleChange = (e) => handleFile(e.target.files[0]);

  const clearImage = () => {
    setPreview(null);
    setFileName('');
    if (onImageSelect) onImageSelect(null, null);
  };

  return (
    <div className="rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-[#222426]/5">
        <h2 className="font-display font-semibold text-[#222426] text-lg flex items-center gap-2">
          <MdCloudUpload className="text-[#FAD02C] text-xl" />
          Upload Road Image
        </h2>
        <p className="text-sm text-[#4F504E] mt-1">Upload a road scene image for AI-powered risk analysis</p>
      </div>

      <div className="p-6 space-y-4">
        {/* Upload Zone */}
        <AnimatePresence mode="wait">
          {!preview ? (
            <motion.label
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              htmlFor="image-upload"
              onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              className={`upload-zone flex flex-col items-center justify-center rounded-2xl cursor-pointer transition-all duration-300 py-14 px-8 text-center ${dragOver ? 'drag-over' : ''}`}
            >
              <motion.div
                animate={{ y: dragOver ? -8 : [0, -6, 0] }}
                transition={dragOver ? { duration: 0.2 } : { duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                className="mb-4"
              >
                <div className="w-20 h-20 rounded-2xl bg-[#FAD02C]/10 border border-[#FAD02C]/20 flex items-center justify-center mx-auto">
                  <MdCloudUpload className="text-4xl text-[#E5BD1A]" />
                </div>
              </motion.div>

              <h3 className="text-[#222426] font-semibold mb-2">
                {dragOver ? 'Drop image here' : 'Drag & drop your image'}
              </h3>
              <p className="text-[#4F504E] text-sm mb-6">or click to browse from your device</p>

              <div className="flex items-center gap-3">
                <span className="btn-primary text-sm pointer-events-none">
                  <MdImage />
                  Browse Image
                </span>
                <span className="btn-secondary text-sm pointer-events-none">
                  <MdPhotoCamera />
                  Camera
                </span>
              </div>

              <p className="text-xs text-[#7E7F81] mt-4">Supports: JPG, PNG, WebP · Max 10MB</p>

              <input
                id="image-upload"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleChange}
              />
            </motion.label>
          ) : (
            <motion.div
              key="preview"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="relative rounded-xl overflow-hidden group"
            >
              <img
                src={preview}
                alt="Preview"
                className="w-full h-72 object-cover rounded-xl"
              />
              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl" />

              {/* Remove button */}
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={clearImage}
                className="absolute top-3 right-3 w-8 h-8 rounded-full bg-black/70 backdrop-blur-sm border border-white/20 flex items-center justify-center text-white hover:bg-red-500/80 hover:border-red-500 transition-all duration-200"
              >
                <MdClose className="text-sm" />
              </motion.button>

              {/* File info */}
              <div className="absolute bottom-3 left-3 bg-black/70 backdrop-blur-sm rounded-lg px-3 py-1.5">
                <p className="text-xs text-white font-medium truncate max-w-48">{fileName}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Model Selector */}
        <div>
          <label className="block text-xs font-medium text-[#4F504E] mb-2 uppercase tracking-wider">Select Model</label>
          <select
            id="model-select"
            className="w-full px-4 py-2.5 rounded-xl text-sm text-[#222426] bg-[#FEFEF4] border border-[#222426]/10 focus:outline-none focus:border-[#FAD02C]/50 cursor-pointer appearance-none transition-colors duration-200"
          >
            <option value="efficientnetb0" className="bg-white text-[#222426]">EfficientNetB0 (Recommended)</option>
            <option value="mobilenetv2" className="bg-white text-[#222426]">MobileNetV2 (Fast)</option>
            <option value="cnn" className="bg-white text-[#222426]">CNN (Baseline)</option>
          </select>
        </div>

        {/* Analyze Button */}
        <motion.button
          whileHover={{ scale: preview ? 1.02 : 1 }}
          whileTap={{ scale: preview ? 0.98 : 1 }}
          className={`w-full py-3 rounded-xl font-semibold text-sm transition-all duration-300 ${preview
            ? 'btn-primary justify-center'
            : 'bg-[#222426]/5 text-[#7E7F81] cursor-not-allowed border border-[#222426]/10'
            }`}
          disabled={!preview}
          id="analyze-button"
        >
          {preview ? '🔍 Analyze Risk' : 'Upload an image to analyze'}
        </motion.button>
      </div>
    </div>
  );
}

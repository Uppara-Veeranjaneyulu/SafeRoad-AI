import { motion } from 'framer-motion';
import { FaGithub } from 'react-icons/fa';
import { MdOpenInNew } from 'react-icons/md';

const coreFeatures = [
  {
    title: 'Proactive Alert System',
    desc: 'Identifies potential hazards and estimates risk levels in milliseconds, shifting road safety from post-accident response to active accident prevention.',
    icon: '⚡',
  },
  {
    title: 'Edge AI Compatibility',
    desc: 'Optimized model weights (MobileNetV2 and EfficientNetB0) allow seamless integration onto low-power edge hardware like dashcams and onboard computers.',
    icon: '📱',
  },
  {
    title: 'Hybrid Inference Pipeline',
    desc: 'Combines real-time YOLOv8 object counts (pedestrians, vehicles) with CNN scene classification for a comprehensive risk-level assessment.',
    icon: '🔗',
  },
  {
    title: 'Weather & Lighting Robustness',
    desc: 'Trained on BDD100K and IDD datasets to perform reliably under rain, night conditions, fog, and unstructured traffic scenarios.',
    icon: '🌤️',
  },
];

const realWorldApplications = [
  {
    title: 'Smart City Infrastructure',
    desc: 'Deployable on municipal CCTV networks to analyze traffic patterns, flag high-risk intersections in real-time, and assist urban planners in improving road design.',
    icon: '🏢',
    color: '#E5BD1A',
  },
  {
    title: 'ADAS Integration',
    desc: 'Can be embedded into Advanced Driver Assistance Systems (ADAS) in consumer cars to trigger instant visual and audio warnings when approaching dangerous scenarios.',
    icon: '🚗',
    color: '#4F504E',
  },
  {
    title: 'Autonomous Vehicles',
    desc: 'Serves as a critical environment risk-classifier layer in self-driving vehicles, enabling AI controllers to adapt speed and caution dynamically based on scene complexity.',
    icon: '🤖',
    color: '#7E7F81',
  },
  {
    title: 'Fleet Safety Monitoring',
    desc: 'Empowers logistics companies to continuously monitor route risk, track driver behavior, and reduce operational liabilities across large commercial fleets.',
    icon: '🚛',
    color: '#E5BD1A',
  },
];


export default function About() {
  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <span className="text-xs font-semibold text-[#E5BD1A] uppercase tracking-widest mb-3 block"></span>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">About SafeRoad AI</h1>
          <p className="text-[#4F504E] max-w-2xl mx-auto">
            An AI-powered road safety platform built to detect, analyze, and prevent accident-prone scenarios using deep learning.
          </p>
          <div className="mt-5 flex items-center justify-center gap-3 flex-wrap">
            <a
              href="https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-xs font-semibold px-4 py-2.5 rounded-lg text-[#FEFEF4] bg-[#222426] hover:opacity-80 transition-all duration-300 shadow-sm"
            >
              <FaGithub /> GitHub Code
            </a>
            <a
              href="https://ieee-dataport.org/documents/saferoad-ai-multi-source-accident-risk-classification-dataset-0"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-xs font-semibold px-4 py-2.5 rounded-lg text-black bg-[#FAD02C] hover:bg-[#E5BD1A] transition-all duration-300 shadow-sm border border-[#222426]/10"
            >
              <MdOpenInNew /> IEEE Dataport Dataset
            </a>
          </div>
        </motion.div>

        {/* Problem Statement */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-8 mb-8 relative overflow-hidden border border-[#F44336]/20 shadow-sm"
          style={{ background: 'linear-gradient(135deg, rgba(244,67,54,0.05) 0%, #FAF9F2 100%)' }}
        >
          <div className="absolute top-0 right-0 w-40 h-40 rounded-bl-full opacity-5 bg-[#F44336]" />
          <h2 className="font-display font-bold text-[#222426] text-2xl mb-4 flex items-center gap-2">
            <span className="text-2xl"></span> Problem Statement
          </h2>
          <p className="text-[#4F504E] leading-relaxed mb-4">
            Road traffic accidents remain one of the leading causes of death and injury worldwide. According to WHO (2023),
            approximately <strong className="text-[#222426]">1.19 million people die each year</strong> due to road traffic crashes,
            with millions more suffering non-fatal injuries.
          </p>
          <p className="text-[#4F504E] leading-relaxed">
            Traditional traffic monitoring systems are <strong className="text-[#222426]">reactive</strong> they detect accidents after they occur.
            SafeRoad AI shifts this paradigm to a <strong className="text-[#E5BD1A] font-semibold">proactive approach</strong>, leveraging deep learning to
            predict high-risk scenarios before accidents happen, enabling timely preventive action.
          </p>
        </motion.div>

        {/* Motivation Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-8 mb-8 bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
        >
          <h2 className="font-display font-bold text-[#222426] text-2xl mb-4">Why It Matters</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { stat: '1.19M', label: 'Deaths per year from road accidents (WHO, 2023)', color: '#D32F2F' },
              { stat: '#3', label: 'Leading cause of death for ages 5–29 globally', color: '#D49A00' },
              { stat: '3–5×', label: 'More accidents in developing nations vs. developed', color: '#4F504E' },
            ].map(({ stat, label, color }) => (
              <div key={stat} className="text-center rounded-xl p-5 bg-[#FEFEF4]" style={{ border: `1px solid ${color}15` }}>
                <p className="font-display font-bold text-3xl mb-2" style={{ color }}>{stat}</p>
                <p className="text-sm text-[#7E7F81]">{label}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* How SafeRoad AI Works */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-8 mb-8 bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
        >
          <div className="text-center mb-10">
            <h2 className="font-display font-bold text-[#222426] text-2xl mb-2">How SafeRoad AI Works</h2>
            <p className="text-sm text-[#7E7F81]">4 simple steps — from a road photo to a safety decision</p>
          </div>

          {/* Steps with connectors */}
          <div className="flex flex-col lg:flex-row items-stretch justify-center gap-0">
            {[
              {
                step: 1,
                img: '/step1_capture.png',
                title: 'Capture',
                desc: 'A dashcam or roadside camera captures a live photo of the road ahead.',
                accent: '#FAD02C',
              },
              {
                step: 2,
                img: '/step2_detect.png',
                title: 'Detect Objects',
                desc: 'YOLOv8 scans the image and spots vehicles, pedestrians, and road hazards.',
                accent: '#00A843',
              },
              {
                step: 3,
                img: '/step3_analyse.png',
                title: 'AI Analysis',
                desc: 'EfficientNetB0 deep learning model analyses the full scene to judge danger.',
                accent: '#1E88E5',
              },
              {
                step: 4,
                img: '/step4_alert.png',
                title: 'Risk Alert',
                desc: 'A clear Low / Medium / High risk result is shown — instantly.',
                accent: '#E53935',
              },
            ].map((item, i, arr) => (
              <div key={i} className="flex flex-col lg:flex-row items-center flex-1">
                {/* Card */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.12 }}
                  className="rounded-2xl overflow-hidden bg-[#FEFEF4] border border-[#222426]/10 shadow-md hover:shadow-xl transition-all duration-300 flex flex-col w-full lg:w-auto lg:flex-1"
                >
                  {/* Image area */}
                  <div className="relative h-44 overflow-hidden">
                    <img
                      src={item.img}
                      alt={item.title}
                      className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                    <div
                      className="absolute top-3 left-3 w-8 h-8 rounded-full flex items-center justify-center text-sm font-black text-white shadow-lg"
                      style={{ background: item.accent }}
                    >
                      {item.step}
                    </div>
                    <div className="absolute bottom-3 left-3">
                      <h3 className="font-display font-bold text-white text-base drop-shadow">{item.title}</h3>
                    </div>
                  </div>
                  <div className="p-4 flex-1">
                    <div className="w-8 h-1 rounded-full mb-3" style={{ background: item.accent }} />
                    <p className="text-xs text-[#4F504E] leading-relaxed">{item.desc}</p>
                  </div>
                </motion.div>

                {/* Connector arrow */}
                {i < arr.length - 1 && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.5 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.12 + 0.18, type: 'spring', bounce: 0.4 }}
                    className="flex items-center justify-center shrink-0 my-3 lg:my-0 lg:mx-2"
                  >
                    <div className="flex lg:hidden flex-col items-center gap-1">
                      <div className="w-0.5 h-5 bg-[#FAD02C]/40" />
                      <svg width="16" height="10" viewBox="0 0 16 10" fill="none">
                        <path d="M8 10L0 0h16L8 10z" fill="#FAD02C" opacity="0.7" />
                      </svg>
                    </div>
                    <div className="hidden lg:flex flex-col items-center gap-1">
                      <div className="flex items-center gap-1">
                        <div className="h-0.5 w-6 bg-gradient-to-r from-[#FAD02C]/30 to-[#FAD02C]" />
                        <svg width="10" height="16" viewBox="0 0 10 16" fill="none">
                          <path d="M10 8L0 0v16L10 8z" fill="#FAD02C" />
                        </svg>
                      </div>
                      <span className="text-[9px] text-[#FAD02C]/60 font-semibold tracking-widest uppercase">Next</span>
                    </div>
                  </motion.div>
                )}
              </div>
            ))}
          </div>

          {/* Result legend */}
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <span className="text-xs text-[#7E7F81] font-semibold">Final output:</span>
            {[
              { label: '🟢 Low Risk', desc: 'Safe to proceed', bg: '#E8F5E9', color: '#00A843' },
              { label: '🟡 Medium Risk', desc: 'Drive with caution', bg: '#FFF8E1', color: '#D49A00' },
              { label: '🔴 High Risk', desc: 'Stop or slow down', bg: '#FCE4EC', color: '#E53935' },
            ].map((r) => (
              <div key={r.label} className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold" style={{ background: r.bg, color: r.color, border: `1px solid ${r.color}30` }}>
                {r.label}
                <span className="font-normal text-[#7E7F81]">— {r.desc}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Key System Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-8 mb-8 bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
        >
          <div className="text-center mb-8">
            <h2 className="font-display font-bold text-[#222426] text-2xl mb-2">Key System Features</h2>
            <p className="text-sm text-[#7E7F81]">What makes SafeRoad AI powerful</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {[
              {
                img: '/feat_proactive_alert.png',
                accent: '#FAD02C',
                title: 'Proactive Alerts',
                tag: '⚡ Real-time',
                desc: 'Spots danger before it becomes an accident — in milliseconds.',
              },
              {
                img: '/feat_edge_ai.png',
                accent: '#1E88E5',
                title: 'Runs on Any Device',
                tag: '📱 Edge AI',
                desc: 'Lightweight enough to run on dashcams and embedded hardware.',
              },
              {
                img: '/feat_hybrid_pipeline.png',
                accent: '#00A843',
                title: 'Smarter Together',
                tag: '🔗 Hybrid Model',
                desc: 'Combines object detection + scene understanding for deeper insight.',
              },
              {
                img: '/feat_weather_robust.png',
                accent: '#E53935',
                title: 'Works in Any Weather',
                tag: '🌧️ All Conditions',
                desc: 'Trained on night, rain, fog and unstructured road scenarios.',
              },
            ].map((feat, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="rounded-2xl overflow-hidden bg-[#FEFEF4] border border-[#222426]/10 shadow-md hover:shadow-xl transition-all duration-300 flex flex-col"
              >
                <div className="relative h-44 overflow-hidden">
                  <img src={feat.img} alt={feat.title} className="w-full h-full object-cover transition-transform duration-500 hover:scale-105" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/65 to-transparent" />
                  <div className="absolute bottom-3 left-3 right-3">
                    <span className="inline-block text-[10px] font-bold px-2 py-0.5 rounded-full mb-1" style={{ background: feat.accent, color: '#222426' }}>{feat.tag}</span>
                    <h3 className="font-display font-bold text-white text-sm drop-shadow">{feat.title}</h3>
                  </div>
                </div>
                <div className="p-4">
                  <div className="w-8 h-1 rounded-full mb-2" style={{ background: feat.accent }} />
                  <p className="text-xs text-[#4F504E] leading-relaxed">{feat.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Real-World Applications */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl p-8 bg-[#FAF9F2] border border-[#222426]/10 shadow-sm"
        >
          <div className="text-center mb-8">
            <h2 className="font-display font-bold text-[#222426] text-2xl mb-2">Real-World Applications</h2>
            <p className="text-sm text-[#7E7F81]">Where SafeRoad AI is already making a difference</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                img: '/app_smart_city.png',
                accent: '#FAD02C',
                title: 'Smart Cities',
                tag: '🏙️ Urban',
                desc: 'Analyses city CCTV to flag dangerous intersections in real time.',
              },
              {
                img: '/app_adas.png',
                accent: '#1E88E5',
                title: 'Car Safety Systems',
                tag: '🚗 ADAS',
                desc: 'Triggers instant visual & audio warnings inside your vehicle.',
              },
              {
                img: '/app_autonomous.png',
                accent: '#00A843',
                title: 'Self-Driving Cars',
                tag: '🤖 Autonomous',
                desc: 'Helps AI drivers adapt speed based on real-time scene risk.',
              },
              {
                img: '/app_fleet.png',
                accent: '#E53935',
                title: 'Fleet Monitoring',
                tag: '🚛 Logistics',
                desc: 'Keeps commercial fleets safe by scoring route and driver risk.',
              },
            ].map((app, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="rounded-2xl overflow-hidden bg-[#FEFEF4] border border-[#222426]/10 shadow-md hover:shadow-xl transition-all duration-300 flex flex-col"
              >
                <div className="relative h-44 overflow-hidden">
                  <img src={app.img} alt={app.title} className="w-full h-full object-cover transition-transform duration-500 hover:scale-105" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/65 to-transparent" />
                  <div className="absolute bottom-3 left-3 right-3">
                    <span className="inline-block text-[10px] font-bold px-2 py-0.5 rounded-full mb-1" style={{ background: app.accent, color: '#222426' }}>{app.tag}</span>
                    <h3 className="font-display font-bold text-white text-sm drop-shadow">{app.title}</h3>
                  </div>
                </div>
                <div className="p-4">
                  <div className="w-8 h-1 rounded-full mb-2" style={{ background: app.accent }} />
                  <p className="text-xs text-[#4F504E] leading-relaxed">{app.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

      </div>
    </div>
  );
}

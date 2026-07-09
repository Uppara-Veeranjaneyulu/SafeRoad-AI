import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MdShield, MdArrowForward } from 'react-icons/md';

// Import local generated images
import heroTrafficImg from '../assets/images/hero_traffic.png';
import roadSafetyProductsImg from '../assets/images/road_safety_products.png';
import dashboardServicesImg from '../assets/images/dashboard_services.png';

const newsArticles = [
  {
    id: 1,
    category: 'Engineering Update',
    title: 'SafeRoad AI Deploys Real-Time Edge Inference Pipeline (Sub-200ms)',
    image: heroTrafficImg,
  },
  {
    id: 2,
    category: 'Research Update',
    title: 'Ensemble Training: BDD100K + Indian Driving Dataset Fused Successfully',
    image: roadSafetyProductsImg,
  },
  {
    id: 3,
    category: 'Product Release',
    title: 'New High-Contrast Minimal User Interface Launched for Public Testing',
    image: dashboardServicesImg,
  },
];

export default function Home() {
  const [productsOpen, setProductsOpen] = useState(false);
  const [servicesOpen, setServicesOpen] = useState(false);

  return (
    <main className="w-full bg-[#FEFEF4] text-[#222426]">
      {/* ─── Hero Section ─── */}
      <section className="relative h-[65vh] md:h-[75vh] lg:h-[80vh] w-full flex items-center justify-center overflow-hidden">
        {/* Background Image */}
        <div className="absolute inset-0">
          <img
            src={heroTrafficImg}
            alt="Futuristic road traffic monitoring"
            className="w-full h-full object-cover"
          />
        </div>
        {/* Forest Deep Green Overlay */}
        <div className="absolute inset-0 bg-[#263B2A]/65 z-10" />

        {/* Hero Content */}
        <div className="relative z-20 max-w-7xl mx-auto px-6 w-full flex flex-col items-start pt-16">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-[90%] md:max-w-[70%]"
          >
            <h1 className="font-display font-bold text-3xl sm:text-5xl lg:text-6xl text-[#FEFEF4] leading-[1.1] tracking-tight">
              We provide better <u className="decoration-[#FAD02C] decoration-[3px] md:decoration-[6px]">quality of life</u> through intelligent road safety AI.
            </h1>

            <Link
              to="/prediction"
              className="mt-8 md:mt-10 group inline-flex items-center gap-3 bg-[#FAD02C] hover:bg-[#E5BD1A] text-black font-semibold px-6 py-3.5 rounded-full transition-all duration-300 shadow-[0_4px_15px_rgba(250,208,44,0.35)]"
              id="hero-get-started"
            >
              <span className="text-sm">Discover SafeRoad AI</span>
              <div className="w-5 h-5 flex items-center justify-center overflow-hidden relative">
                <MdArrowForward className="text-lg transition-transform duration-300 group-hover:translate-x-1" />
              </div>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* ─── Intro Section ─── */}
      <section className="max-w-7xl mx-auto px-6 py-12 md:py-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <div className="lg:col-span-6">
            <h2 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] leading-tight">
              For every life. On every journey.
            </h2>
          </div>
          <div className="lg:col-span-6">
            <p className="text-base sm:text-lg text-[#4F504E] leading-relaxed">
              We are developing intelligent solutions for modern transport networks. By leveraging deep learning models, YOLOv8 object detection, and risk classification architectures, we analyze road scenes to help prevent accidents and make driving safer.
            </p>
          </div>
        </div>
      </section>

      {/* ─── Collapsible Categories (Accordions) ─── */}
      <section className="w-full border-t border-[#222426]/10">
        {/* Products Accordion */}
        <div className="w-full border-b border-[#222426]/10 bg-[#FEFEF4] hover:bg-[#FAF9F2] transition-colors duration-300">
          <div className="max-w-7xl mx-auto px-6 py-8 md:py-12">
            <button
              onClick={() => setProductsOpen(!productsOpen)}
              className="w-full flex items-center justify-between text-left group"
            >
              <div>
                <span className="text-xs uppercase tracking-[0.125rem] text-[#222426]/60 font-semibold block mb-1">
                  What we offer
                </span>
                <h3 className="font-display font-bold text-2xl sm:text-4xl text-[#222426]">
                  Products
                </h3>
              </div>
              <div className="w-10 h-10 md:w-14 md:h-14 rounded-full border border-[#222426]/20 flex items-center justify-center group-hover:border-[#222426] transition-colors duration-300">
                <svg
                  className={`w-4 h-4 md:w-6 md:h-6 transform transition-transform duration-300 ${productsOpen ? 'rotate-180' : ''
                    }`}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                >
                  <path d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </button>

            {/* Accordion Content */}
            {productsOpen && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                transition={{ duration: 0.4 }}
                className="mt-8 pt-6 border-t border-[#222426]/5 overflow-hidden"
              >
                <p className="text-[#4F504E] text-sm md:text-base mb-6">
                  Discover our advanced traffic safety modules
                </p>
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 items-stretch">
                  <Link
                    to="/prediction"
                    className="flex flex-col justify-between p-6 h-[9rem] bg-[#FAD02C]/10 hover:bg-[#FAD02C]/20 border border-[#FAD02C]/20 transition-all duration-300 group"
                  >
                    <div className="text-lg font-bold text-[#222426]">Road Scene Classification</div>
                    <div className="flex justify-end">
                      <MdArrowForward className="text-xl transition-transform duration-300 group-hover:translate-x-1" />
                    </div>
                  </Link>
                  <Link
                    to="/prediction"
                    className="flex flex-col justify-between p-6 h-[9rem] bg-[#FAD02C]/10 hover:bg-[#FAD02C]/20 border border-[#FAD02C]/20 transition-all duration-300 group"
                  >
                    <div className="text-lg font-bold text-[#222426]">YOLOv8 Real-Time Detection</div>
                    <div className="flex justify-end">
                      <MdArrowForward className="text-xl transition-transform duration-300 group-hover:translate-x-1" />
                    </div>
                  </Link>
                  <Link
                    to="/prediction"
                    className="flex flex-col justify-between p-6 h-[9rem] bg-[#FAD02C]/10 hover:bg-[#FAD02C]/20 border border-[#FAD02C]/20 transition-all duration-300 group"
                  >
                    <div className="text-lg font-bold text-[#222426]">Ensemble Risk Assessment</div>
                    <div className="flex justify-end">
                      <MdArrowForward className="text-xl transition-transform duration-300 group-hover:translate-x-1" />
                    </div>
                  </Link>
                  <div className="h-[9rem] overflow-hidden">
                    <img
                      src={roadSafetyProductsImg}
                      alt="Traffic sensors hardware"
                      className="w-full h-full object-cover rounded-sm"
                    />
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Services Accordion */}
        <div className="w-full border-b border-[#222426]/10 bg-[#FEFEF4] hover:bg-[#FAF9F2] transition-colors duration-300">
          <div className="max-w-7xl mx-auto px-6 py-8 md:py-12">
            <button
              onClick={() => setServicesOpen(!servicesOpen)}
              className="w-full flex items-center justify-between text-left group"
            >
              <div>
                <span className="text-xs uppercase tracking-[0.125rem] text-[#222426]/60 font-semibold block mb-1">
                  We can help you with
                </span>
                <h3 className="font-display font-bold text-2xl sm:text-4xl text-[#222426]">
                  Services
                </h3>
              </div>
              <div className="w-10 h-10 md:w-14 md:h-14 rounded-full border border-[#222426]/20 flex items-center justify-center group-hover:border-[#222426] transition-colors duration-300">
                <svg
                  className={`w-4 h-4 md:w-6 md:h-6 transform transition-transform duration-300 ${servicesOpen ? 'rotate-180' : ''
                    }`}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                >
                  <path d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </button>

            {/* Accordion Content */}
            {servicesOpen && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                transition={{ duration: 0.4 }}
                className="mt-8 pt-6 border-t border-[#222426]/5 overflow-hidden"
              >
                <p className="text-[#4F504E] text-sm md:text-base mb-6">
                  Explore our core visualization and analytics services
                </p>
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 items-stretch">
                  <Link
                    to="/dashboard"
                    className="flex flex-col justify-between p-6 h-[9rem] bg-[#EBEAE5]/30 hover:bg-[#EBEAE5]/60 border border-[#222426]/10 transition-all duration-300 group"
                  >
                    <div className="text-lg font-bold text-[#222426]">Interactive Safety Dashboard</div>
                    <div className="flex justify-end">
                      <MdArrowForward className="text-xl transition-transform duration-300 group-hover:translate-x-1" />
                    </div>
                  </Link>
                  <Link
                    to="/analytics"
                    className="flex flex-col justify-between p-6 h-[9rem] bg-[#EBEAE5]/30 hover:bg-[#EBEAE5]/60 border border-[#222426]/10 transition-all duration-300 group"
                  >
                    <div className="text-lg font-bold text-[#222426]">Model Performance Analytics</div>
                    <div className="flex justify-end">
                      <MdArrowForward className="text-xl transition-transform duration-300 group-hover:translate-x-1" />
                    </div>
                  </Link>
                  <Link
                    to="/datasets"
                    className="flex flex-col justify-between p-6 h-[9rem] bg-[#EBEAE5]/30 hover:bg-[#EBEAE5]/60 border border-[#222426]/10 transition-all duration-300 group"
                  >
                    <div className="text-lg font-bold text-[#222426]">Curated Road Datasets</div>
                    <div className="flex justify-end">
                      <MdArrowForward className="text-xl transition-transform duration-300 group-hover:translate-x-1" />
                    </div>
                  </Link>
                  <div className="h-[9rem] overflow-hidden">
                    <img
                      src={dashboardServicesImg}
                      alt="Dashboard visualization analytics"
                      className="w-full h-full object-cover rounded-sm"
                    />
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </section>

      {/* ─── Latest News Section ─── */}
      <section className="bg-[#FAF9F2] w-full py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between mb-12">
            <h2 className="font-display font-bold text-2xl sm:text-4xl text-[#222426]">
              Latest updates
            </h2>
            <Link
              to="/about"
              className="flex items-center gap-2 text-sm font-semibold text-[#222426] hover:underline hover:decoration-[#FAD02C] hover:decoration-2"
            >
              See all updates <MdArrowForward className="text-base text-[#FAD02C]" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {newsArticles.map((article) => (
              <article key={article.id} className="group cursor-pointer">
                <div className="flex flex-col h-full">
                  <div className="w-full h-48 md:h-56 overflow-hidden relative rounded-lg">
                    <img
                      src={article.image}
                      alt={article.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                    />
                  </div>
                  <span className="text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mt-4">
                    {article.category}
                  </span>
                  <h3 className="font-display font-bold text-lg text-[#222426] mt-2 group-hover:text-[#E5BD1A] transition-colors duration-300 leading-snug">
                    {article.title}
                  </h3>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

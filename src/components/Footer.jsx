import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MdShield, MdEmail, MdCode } from 'react-icons/md';
import { FaGithub, FaLinkedin, FaTwitter } from 'react-icons/fa';

const footerLinks = {
  Platform: [
    { label: 'Home', to: '/' },
    { label: 'Dashboard', to: '/dashboard' },
    { label: 'Prediction', to: '/prediction' },
    { label: 'Model Analytics', to: '/analytics' },
  ],
  Research: [
    { label: 'Datasets', to: '/datasets' },
    { label: 'About', to: '/about' },
  ],
  Resources: [
    { label: 'Documentation', to: '#' },
    { label: 'API Reference', to: '#' },
    { label: 'Privacy Policy', to: '#' },
    { label: 'Contact', to: '/contact' },
  ],
};

export default function Footer() {
  return (
    <footer className="relative bg-[#222426] text-[#FEFEF4]/80 border-t border-white/5">
      {/* Top safety-yellow accent line */}
      <div className="h-1 bg-gradient-to-r from-transparent via-[#FAD02C]/70 to-transparent" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <Link to="/" className="flex items-center gap-2.5 mb-4 group">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#FAD02C] to-[#E5BD1A] flex items-center justify-center shadow-[0_0_10px_rgba(250,208,44,0.2)]">
                <MdShield className="text-[#222426] text-xl" />
              </div>
              <span className="font-display font-bold text-lg text-white">
                SafeRoad<span className="text-[#FAD02C]"> AI</span>
              </span>
            </Link>
            <p className="text-sm text-gray-400 leading-relaxed mb-6 max-w-xs">
              Deep Learning-Based Road Scene Risk Classification and Traffic Monitoring for Proactive Road Safety.
            </p>
            <p className="text-xs font-semibold text-[#FAD02C] tracking-widest uppercase mb-4">
              "Predict Risks. Prevent Accidents."
            </p>

            {/* Social Links */}
            <div className="flex items-center gap-3">
              {[
                { icon: FaGithub, href: 'https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI', label: 'GitHub' },
                { icon: MdEmail, href: 'mailto:uupparaveeranji@gmail.com', label: 'Email' },
              ].map(({ icon: Icon, href, label }) => (
                <motion.a
                  key={label}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ y: -3, scale: 1.05 }}
                  className="w-9 h-9 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-[#FAD02C] hover:border-[#FAD02C]/30 hover:bg-white/10 transition-colors duration-200"
                  aria-label={label}
                >
                  <Icon className="text-sm" />
                </motion.a>
              ))}
            </div>
          </div>

          {/* Links Grid */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="text-xs font-semibold text-white/40 uppercase tracking-widest mb-4">
                {category}
              </h4>
              <ul className="space-y-2.5">
                {links.map((link) => (
                  <li key={link.label}>
                    <Link
                      to={link.to}
                      className="text-sm text-gray-400 hover:text-white hover:underline hover:underline-offset-4 hover:decoration-[#FAD02C] transition-all duration-200 inline-block"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar with yellow stripe */}
        <div className="mt-12 pt-6 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-gray-500">
            © 2026 SafeRoad AI. All rights reserved. Built with inspiration from road safety infrastructure standards.
          </p>
          <div className="flex items-center gap-4 text-xs text-gray-500">
            <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
            <span>·</span>
            <a href="#" className="hover:text-white transition-colors">Terms of Use</a>
            <span>·</span>
            <a
              href="https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 hover:text-white transition-colors text-gray-500"
            >
              <MdCode className="text-sm" />
              Open Source
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

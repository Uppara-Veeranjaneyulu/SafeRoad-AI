import { useState, useEffect } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MdShield,
  MdMenu,
  MdClose,
  MdCode,
} from 'react-icons/md';

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/prediction', label: 'Prediction' },
  { to: '/analytics', label: 'Model Analytics' },
  { to: '/datasets', label: 'Datasets' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' },
];

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
  }, [location]);

  return (
    <>
      <motion.nav
        initial={{ y: -80, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled
          ? 'bg-[#222426] border-b border-white/5 shadow-[0_4px_30px_rgba(0,0,0,0.15)]'
          : 'bg-transparent bg-gradient-to-b from-[#222426]/80 to-transparent'
          }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2.5 group">
              <div className="relative">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#FAD02C] to-[#E5BD1A] flex items-center justify-center shadow-[0_0_15px_rgba(250,208,44,0.3)] group-hover:shadow-[0_0_25px_rgba(250,208,44,0.5)] transition-shadow duration-300">
                  <MdShield className="text-[#222426] text-xl" />
                </div>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="font-display font-bold text-lg tracking-tight text-white leading-none">SafeRoad</span>
                <span className="inline-flex items-center px-1.5 py-0.5 rounded-md bg-[#FAD02C] text-[#222426] text-[10px] font-black tracking-widest uppercase leading-none shadow-sm">AI</span>
              </div>
            </Link>

            {/* Desktop Nav Links */}
            <div className="hidden lg:flex items-center gap-6">
              {navLinks.map((link) => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  end={link.to === '/'}
                  className={({ isActive }) =>
                    `text-sm font-medium transition-all duration-200 text-[#FEFEF4]/80 hover:text-white hover:underline hover:underline-offset-4 hover:decoration-[#FAD02C] hover:decoration-2 ${isActive
                      ? 'text-white underline underline-offset-4 decoration-[#FAD02C] decoration-2'
                      : ''
                    }`
                  }
                >
                  {link.label}
                </NavLink>
              ))}
            </div>

            {/* Right Controls */}
            <div className="flex items-center gap-3">
              {/* GitHub Link as Yellow Pill Button */}
              <a
                href="https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI"
                target="_blank"
                rel="noopener noreferrer"
                className="hidden sm:flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-semibold text-black bg-[#FAD02C] hover:bg-[#E5BD1A] transition-all duration-200 shadow-sm"
                id="github-button"
              >
                <MdCode className="text-sm" />
                GitHub
              </a>

              {/* Mobile Menu Toggle */}
              <button
                onClick={() => setMobileOpen(!mobileOpen)}
                className="lg:hidden p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all duration-200"
                aria-label="Toggle mobile menu"
                id="mobile-menu-toggle"
              >
                {mobileOpen ? <MdClose className="text-xl" /> : <MdMenu className="text-xl" />}
              </button>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Mobile Menu Drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, x: '100%' }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed inset-y-0 right-0 z-40 w-72 bg-[#222426] border-l border-white/5 lg:hidden"
          >
            <div className="flex flex-col h-full pt-20 pb-8 px-6">
              <div className="flex flex-col gap-1">
                {navLinks.map((link, i) => (
                  <motion.div
                    key={link.to}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                  >
                    <NavLink
                      to={link.to}
                      end={link.to === '/'}
                      className={({ isActive }) =>
                        `flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 text-[#FEFEF4]/80 hover:text-white hover:bg-white/5 ${isActive
                          ? 'text-white bg-white/5 border border-white/10'
                          : ''
                        }`
                      }
                    >
                      {link.label}
                    </NavLink>
                  </motion.div>
                ))}
              </div>

              <div className="mt-auto pt-6 border-t border-white/5">
                <a
                  href="https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-sm font-medium text-black bg-[#FAD02C] hover:bg-[#E5BD1A] transition-all duration-200"
                >
                  <MdCode className="text-base" />
                  View on GitHub
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Mobile Overlay */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setMobileOpen(false)}
            className="fixed inset-0 z-30 bg-black/60 lg:hidden"
          />
        )}
      </AnimatePresence>
    </>
  );
}

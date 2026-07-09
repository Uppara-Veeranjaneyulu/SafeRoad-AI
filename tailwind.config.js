/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
       colors: {
        primary: {
          DEFAULT: '#222426', // Charcoal
          light: '#333537',
          dark: '#1A1C1E',
        },
        secondary: '#FEFEF4', // Warm White
        accent: {
          DEFAULT: '#FAD02C', // Safety Yellow
          dark: '#E5BD1A',
          glow: 'rgba(250, 208, 44, 0.3)',
        },
        charcoal: {
          DEFAULT: '#222426',
          80: '#333537',
          60: '#4F504E',
        },
        'warm-white': {
          DEFAULT: '#FEFEF4',
          80: '#FAF9F2',
        },
        'safety-yellow': {
          DEFAULT: '#FAD02C',
          dark: '#E5BD1A',
        },
        warning: '#FFC107',
        danger: '#F44336',
        glass: 'rgba(255, 255, 255, 0.05)',
        'glass-border': 'rgba(255, 255, 255, 0.08)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Space Grotesk', 'Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(135deg, #1A1C1E 0%, #222426 50%, #333537 100%)',
        'card-gradient': 'linear-gradient(135deg, rgba(34, 36, 38, 0.04) 0%, rgba(34, 36, 38, 0.01) 100%)',
        'accent-gradient': 'linear-gradient(135deg, #FAD02C 0%, #E5BD1A 100%)',
        'danger-gradient': 'linear-gradient(135deg, #F44336 0%, #FF5252 100%)',
        'warning-gradient': 'linear-gradient(135deg, #FFC107 0%, #FFD54F 100%)',
      },
      boxShadow: {
        'glass': '0 8px 32px rgba(0, 0, 0, 0.1)',
        'glow-accent': '0 0 30px rgba(250, 208, 44, 0.3)',
        'glow-blue': '0 0 30px rgba(34, 36, 38, 0.15)',
        'card': '0 4px 24px rgba(0, 0, 0, 0.06)',
        'neon': '0 0 20px rgba(250, 208, 44, 0.5), 0 0 40px rgba(250, 208, 44, 0.2)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'slide-up': 'slideUp 0.6s ease-out',
        'fade-in': 'fadeIn 0.8s ease-out',
        'spin-slow': 'spin 8s linear infinite',
        'grid-move': 'gridMove 20s linear infinite',
        'counter': 'counter 2s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 200, 83, 0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(0, 200, 83, 0.6)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        gridMove: {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(-50px)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}

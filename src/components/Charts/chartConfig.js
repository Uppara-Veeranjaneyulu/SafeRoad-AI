import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
);

export const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#4F504E',
        font: { family: 'Inter', size: 12 },
        usePointStyle: true,
        pointStyleWidth: 8,
      },
    },
    tooltip: {
      backgroundColor: 'rgba(34, 36, 38, 0.95)',
      borderColor: 'rgba(34, 36, 38, 0.1)',
      borderWidth: 1,
      titleColor: '#FEFEF4',
      bodyColor: '#FAF9F2',
      padding: 12,
      cornerRadius: 10,
    },
  },
  scales: {
    x: {
      grid: { color: 'rgba(34, 36, 38, 0.04)', drawBorder: false },
      ticks: { color: '#7E7F81', font: { family: 'Inter', size: 11 } },
    },
    y: {
      grid: { color: 'rgba(34, 36, 38, 0.04)', drawBorder: false },
      ticks: { color: '#7E7F81', font: { family: 'Inter', size: 11 } },
    },
  },
};

export const noScaleOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#4F504E',
        font: { family: 'Inter', size: 12 },
        usePointStyle: true,
        padding: 16,
      },
    },
    tooltip: {
      backgroundColor: 'rgba(34, 36, 38, 0.95)',
      borderColor: 'rgba(34, 36, 38, 0.1)',
      borderWidth: 1,
      titleColor: '#FEFEF4',
      bodyColor: '#FAF9F2',
      padding: 12,
      cornerRadius: 10,
    },
  },
};

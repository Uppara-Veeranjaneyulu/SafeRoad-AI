import { Line } from 'react-chartjs-2';
import { defaultOptions } from './chartConfig';
import { accuracyCurveData, lossCurveData } from '../../data/dummyData';
import '../Charts/chartConfig';

export function AccuracyCurveChart({ data }) {
  return (
    <div className="chart-wrapper">
      <Line data={data || accuracyCurveData} options={{
        ...defaultOptions,
        scales: {
          ...defaultOptions.scales,
          x: { ...defaultOptions.scales.x, title: { display: true, text: 'Epoch', color: '#64748B' } },
          y: {
            ...defaultOptions.scales.y,
            title: { display: true, text: 'Accuracy (%)', color: '#64748B' },
            ticks: { ...defaultOptions.scales.y.ticks, callback: (v) => `${Number(v).toFixed(0)}%` },
          },
        },
      }} />
    </div>
  );
}

export function LossCurveChart({ data }) {
  return (
    <div className="chart-wrapper">
      <Line data={data || lossCurveData} options={{
        ...defaultOptions,
        scales: {
          ...defaultOptions.scales,
          x: { ...defaultOptions.scales.x, title: { display: true, text: 'Epoch', color: '#64748B' } },
          y: {
            ...defaultOptions.scales.y,
            title: { display: true, text: 'Loss', color: '#64748B' },
            ticks: { ...defaultOptions.scales.y.ticks, callback: (v) => Number(v).toFixed(2) },
          },
        },
      }} />
    </div>
  );
}

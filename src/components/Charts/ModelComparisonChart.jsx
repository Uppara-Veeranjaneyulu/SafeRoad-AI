import { Bar } from 'react-chartjs-2';
import { defaultOptions } from './chartConfig';
import { modelComparisonData } from '../../data/dummyData';
import '../Charts/chartConfig';

export function ModelComparisonChart() {
  return (
    <div className="chart-wrapper">
      <Bar data={modelComparisonData} options={{
        ...defaultOptions,
        scales: {
          ...defaultOptions.scales,
          y: {
            ...defaultOptions.scales.y,
            min: 80,
            max: 100,
            ticks: { ...defaultOptions.scales.y.ticks, callback: (v) => `${v}%` },
          },
        },
      }} />
    </div>
  );
}

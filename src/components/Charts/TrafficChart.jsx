import { Bar } from 'react-chartjs-2';
import { defaultOptions } from './chartConfig';
import { trafficDensityData } from '../../data/dummyData';
import '../Charts/chartConfig';

export function TrafficChart() {
  return (
    <div className="chart-wrapper">
      <Bar data={trafficDensityData} options={{
        ...defaultOptions,
        plugins: {
          ...defaultOptions.plugins,
          legend: { display: false },
        },
        scales: {
          ...defaultOptions.scales,
          y: {
            ...defaultOptions.scales.y,
            ticks: { ...defaultOptions.scales.y.ticks, callback: (v) => `${v}%` },
          },
        },
      }} />
    </div>
  );
}

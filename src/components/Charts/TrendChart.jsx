import { Line } from 'react-chartjs-2';
import { defaultOptions } from './chartConfig';
import { predictionTrendData } from '../../data/dummyData';
import '../Charts/chartConfig';

export function TrendChart() {
  return (
    <div className="chart-wrapper">
      <Line data={predictionTrendData} options={defaultOptions} />
    </div>
  );
}

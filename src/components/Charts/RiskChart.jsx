import { Doughnut } from 'react-chartjs-2';
import { noScaleOptions } from './chartConfig';
import { riskDistributionData } from '../../data/dummyData';
import '../Charts/chartConfig';

export function RiskChart() {
  return (
    <div className="chart-wrapper">
      <Doughnut data={riskDistributionData} options={{
        ...noScaleOptions,
        cutout: '65%',
        plugins: {
          ...noScaleOptions.plugins,
          legend: { ...noScaleOptions.plugins.legend, position: 'bottom' },
        },
      }} />
    </div>
  );
}

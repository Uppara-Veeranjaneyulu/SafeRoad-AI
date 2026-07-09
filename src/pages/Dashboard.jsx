import { motion } from 'framer-motion';
import { MdDashboard, MdImage, MdAnalytics, MdTrendingUp, MdShield, MdSpeed } from 'react-icons/md';
import AnalyticsCard from '../components/AnalyticsCard';
import { RiskChart } from '../components/Charts/RiskChart';
import { TrafficChart } from '../components/Charts/TrafficChart';
import { ModelComparisonChart } from '../components/Charts/ModelComparisonChart';
import { TrendChart } from '../components/Charts/TrendChart';
import { dashboardStats, predictionHistory } from '../data/dummyData';

const riskBadge = (risk) => {
  if (risk === 'Low Risk') return <span className="badge-low">{risk}</span>;
  if (risk === 'Moderate Risk') return <span className="badge-moderate">{risk}</span>;
  return <span className="badge-high">{risk}</span>;
};

function ChartCard({ title, subtitle, children }) {
  return (
    <div className="rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] shadow-sm overflow-hidden">
      <div className="px-5 py-4 border-b border-[#222426]/5">
        <h3 className="font-semibold text-[#222426] text-sm">{title}</h3>
        {subtitle && <p className="text-xs text-[#7E7F81] mt-0.5">{subtitle}</p>}
      </div>
      <div className="p-5">{children}</div>
    </div>
  );
}

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="w-9 h-9 rounded-xl bg-[#FAD02C]/10 border border-[#FAD02C]/30 flex items-center justify-center">
              <MdDashboard className="text-[#E5BD1A] text-lg" />
            </div>
            <div>
              <h1 className="font-display font-bold text-2xl text-[#222426]">Analytics Dashboard</h1>
              <p className="text-sm text-[#4F504E]">Real-time road safety monitoring and prediction analytics</p>
            </div>
          </div>
          <div className="flex items-center gap-2 mt-3">
            <span className="w-2 h-2 rounded-full bg-[#E5BD1A] animate-pulse" />
            <span className="text-xs text-[#E5BD1A] font-medium">Live · Updated 2 minutes ago</span>
          </div>
        </motion.div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <AnalyticsCard title="Total Images Processed" value={dashboardStats.totalImages} icon={MdImage} color="#E5BD1A" trend={8} />
          <AnalyticsCard title="Total Predictions" value={dashboardStats.totalPredictions} icon={MdAnalytics} color="#E5BD1A" trend={12} />
          <AnalyticsCard title="Avg Confidence" value={dashboardStats.avgConfidence} unit="%" icon={MdTrendingUp} color="#4F504E" trend={2} />
          <AnalyticsCard title="Best Model" value={dashboardStats.bestModel} icon={MdSpeed} color="#E5BD1A" isNumber={false} />
          <AnalyticsCard
            title="Latest Prediction"
            value={dashboardStats.latestPrediction.risk}
            icon={MdShield}
            color="#D32F2F"
            isNumber={false}
            subtitle={`${dashboardStats.latestPrediction.confidence}% confidence · ${dashboardStats.latestPrediction.timestamp}`}
          />
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-5">
          <ChartCard title="Risk Level Distribution" subtitle="All predictions categorized by risk">
            <RiskChart />
          </ChartCard>
          <ChartCard title="Traffic Density Distribution" subtitle="Scene traffic patterns across dataset">
            <TrafficChart />
          </ChartCard>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-8">
          <div className="lg:col-span-2">
            <ChartCard title="Weekly Prediction Trend" subtitle="Total predictions and high-risk events over 7 days">
              <TrendChart />
            </ChartCard>
          </div>
          <ChartCard title="Model Performance" subtitle="Accuracy comparison across models">
            <ModelComparisonChart />
          </ChartCard>
        </div>

        {/* Prediction History Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] shadow-sm overflow-hidden"
        >
          <div className="px-6 py-4 border-b border-[#222426]/5 flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-[#222426]">Prediction History</h3>
              <p className="text-xs text-[#7E7F81] mt-0.5">Recent road scene analyses</p>
            </div>
            <span className="text-xs px-3 py-1 rounded-full bg-[#FEFEF4] border border-[#222426]/10 text-[#4F504E] font-medium">
              {predictionHistory.length} records
            </span>
          </div>
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Image</th>
                  <th>Model</th>
                  <th>Risk Level</th>
                  <th>Confidence</th>
                  <th>Traffic</th>
                  <th>Weather</th>
                  <th>Inference</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {predictionHistory.map((row, i) => (
                  <motion.tr
                    key={row.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                  >
                    <td className="font-mono text-xs text-[#7E7F81]">{row.id}</td>
                    <td className="text-[#4F504E] text-xs font-semibold">{row.image}</td>
                    <td>
                      <span className="text-xs px-2 py-1 rounded-md bg-[#FEFEF4] border border-[#222426]/10 text-[#4F504E] font-medium">{row.model}</span>
                    </td>
                    <td>{riskBadge(row.risk)}</td>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-16 rounded-full bg-[#222426]/10 overflow-hidden">
                          <div className="h-full rounded-full bg-[#FAD02C]" style={{ width: `${row.confidence}%` }} />
                        </div>
                        <span className="text-xs text-[#4F504E] font-semibold">{row.confidence}%</span>
                      </div>
                    </td>
                    <td className="text-xs text-[#4F504E] font-medium">{row.traffic}</td>
                    <td className="text-xs text-[#4F504E] font-medium">{row.weather}</td>
                    <td className="font-mono text-xs text-[#00A843] font-semibold">{row.duration}</td>
                    <td className="text-xs text-[#7E7F81]">{row.time}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

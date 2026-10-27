import React from 'react';
import {
  CreditCard,
  AlertTriangle,
  Briefcase,
  CheckCircle2,
  Users,
  ShieldCheck,
  TrendingUp,
  ArrowUpRight,
  ExternalLink,
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { StatCard } from '../components/common/StatCard';
import { SeverityBadge, StatusBadge } from '../components/common/Badge';
import { DashboardSummary, TrendItem, ChannelMetric, Alert } from '../types';
import { NavTab } from '../components/common/Sidebar';

interface DashboardPageProps {
  summary: DashboardSummary | null;
  trends: TrendItem[];
  channels: ChannelMetric[];
  recentAlerts: Alert[];
  onNavigate: (tab: NavTab) => void;
  onOpenCreateTransaction: () => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  summary,
  trends,
  channels,
  recentAlerts,
  onNavigate,
  onOpenCreateTransaction,
}) => {
  const formatINR = (val: number) => {
    // For values >= 1 Crore (₹10,000,000), format in Crores for clean fintech presentation
    if (val >= 10000000) {
      const inCr = val / 10000000;
      return `₹${inCr.toLocaleString('en-IN', { maximumFractionDigits: 2 })} Cr`;
    }
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(val);
  };

  const pieColors = ['#06B6D4', '#3B82F6', '#8B5CF6', '#10B981', '#F59E0B'];

  const channelChartData = channels.map((c) => ({
    name: c.channel,
    volume: c.total_volume,
    count: c.total_tx,
  }));

  return (
    <div className="space-y-6">
      {/* Welcome Banner & Action Bar */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider font-mono">
              Live Surveillance Active
            </span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight mt-1">
            Executive Fraud Surveillance Console
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Real-time financial telemetry backed by Oracle Database 26ai Free. Procedural rules automatically flag anomalous volume and nocturnal velocities exceeding threshold.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onOpenCreateTransaction}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs tracking-wide shadow-md shadow-cyan-500/20 transition-all hover:scale-105 active:scale-95"
          >
            <CreditCard className="w-4 h-4" />
            <span>Post New Transaction</span>
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Ledger Volume"
          value={formatINR(summary?.total_volume_inr || 0)}
          subtitle={
            (summary?.total_volume_inr || 0) >= 10000000
              ? `${summary?.total_transactions || 0} Settled • ₹${(summary?.total_volume_inr || 0).toLocaleString('en-IN')}`
              : `${summary?.total_transactions || 0} Settled Transactions`
          }
          icon={TrendingUp}
          variant="cyan"
          onClick={() => onNavigate('transactions')}
        />
        <StatCard
          title="Flagged Transactions"
          value={summary?.flagged_transactions || 0}
          subtitle={`Breached >₹${(summary?.high_amount_threshold || 50000).toLocaleString('en-IN')} rule`}
          icon={AlertTriangle}
          variant="rose"
          onClick={() => onNavigate('transactions')}
        />
        <StatCard
          title="Surveillance Alerts"
          value={summary?.total_alerts || 0}
          subtitle={`${summary?.critical_alerts || 0} Critical / ${summary?.pending_alerts || 0} Pending`}
          icon={ShieldCheck}
          variant="amber"
          onClick={() => onNavigate('alerts')}
        />
        <StatCard
          title="Active Investigations"
          value={summary?.open_investigations || 0}
          subtitle={`${summary?.closed_investigations || 0} Resolved Cases`}
          icon={Briefcase}
          variant="blue"
          onClick={() => onNavigate('investigations')}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Transaction Volume Timeline */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white tracking-wide">
                Transaction Volume & Anomaly Timeline
              </h2>
              <p className="text-xs text-slate-400">
                Daily settled funds (INR) vs flagged procedural breaches
              </p>
            </div>
            <button
              onClick={() => onNavigate('analytics')}
              className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-medium"
            >
              <span>Detailed Breakdown</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="volGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#06B6D4" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <XAxis
                  dataKey="date"
                  stroke="#475569"
                  fontSize={11}
                  tickLine={false}
                  tickFormatter={(val) => val.slice(5)}
                />
                <YAxis
                  stroke="#475569"
                  fontSize={11}
                  tickLine={false}
                  tickFormatter={(val) => `₹${(val / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0F172A',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                  formatter={(value: any) => [formatINR(Number(value)), 'Total Volume']}
                  labelFormatter={(label) => `Date: ${label}`}
                />
                <Area
                  type="monotone"
                  dataKey="total_volume"
                  stroke="#06B6D4"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#volGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Channel Volume Breakdown */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white tracking-wide">
                Volume by Channel
              </h2>
              <p className="text-xs text-slate-400">Distribution across banking payment rails</p>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={channelChartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#475569" fontSize={10} tickLine={false} />
                <YAxis
                  stroke="#475569"
                  fontSize={10}
                  tickLine={false}
                  tickFormatter={(val) => `${(val / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0F172A',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                  formatter={(val: any) => [formatINR(Number(val)), 'Volume']}
                />
                <Bar dataKey="volume" radius={[4, 4, 0, 0]}>
                  {channelChartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Flagged Alerts Table Preview */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-semibold text-white tracking-wide">
              Recent Surveillance Alerts
            </h2>
            <p className="text-xs text-slate-400">
              Live anomaly alerts generated by PL/SQL stored procedure SP_EVALUATE_AND_ALERT_TRANSACTION
            </p>
          </div>
          <button
            onClick={() => onNavigate('alerts')}
            className="text-xs text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1"
          >
            <span>View All Alerts</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-mono">
                <th className="pb-3 font-semibold">Alert ID</th>
                <th className="pb-3 font-semibold">Triggered Rule</th>
                <th className="pb-3 font-semibold">Customer & Account</th>
                <th className="pb-3 font-semibold">Amount</th>
                <th className="pb-3 font-semibold">Severity</th>
                <th className="pb-3 font-semibold">Status</th>
                <th className="pb-3 font-semibold">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {recentAlerts.slice(0, 5).map((a) => (
                <tr key={a.alert_id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 font-mono font-bold text-cyan-400">#{a.alert_id}</td>
                  <td className="py-3 font-medium text-slate-200">{a.rule_triggered}</td>
                  <td className="py-3 text-slate-300">
                    <div>{a.customer_name || 'N/A'}</div>
                    <div className="text-[10px] font-mono text-slate-500">{a.account_number}</div>
                  </td>
                  <td className="py-3 font-mono font-semibold text-white">
                    {a.amount ? formatINR(a.amount) : 'N/A'}
                  </td>
                  <td className="py-3">
                    <SeverityBadge severity={a.severity} />
                  </td>
                  <td className="py-3">
                    <StatusBadge status={a.status} />
                  </td>
                  <td className="py-3 text-slate-400 font-mono text-[11px]">{a.alert_date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

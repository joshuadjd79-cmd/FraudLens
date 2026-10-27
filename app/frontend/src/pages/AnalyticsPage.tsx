import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  PieChart,
  TrendingUp,
  Download,
  AlertTriangle,
  ShieldCheck,
  Users,
  CheckCircle2,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  Pie,
} from 'recharts';
import { CustomerExposure, ChannelMetric, DashboardSummary } from '../types';
import { api } from '../api/client';

export const AnalyticsPage: React.FC = () => {
  const [exposureData, setExposureData] = useState<CustomerExposure[]>([]);
  const [channelData, setChannelData] = useState<ChannelMetric[]>([]);
  const [severities, setSeverities] = useState<{ severity: string; count: number }[]>([]);
  const [outcomes, setOutcomes] = useState<{ outcome: string; count: number }[]>([]);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        setIsLoading(true);
        const [summaryRes, exposureRes] = await Promise.all([
          api.getAnalyticsSummary(),
          api.getCustomerExposure(),
        ]);
        setSummary(summaryRes.kpis);
        setChannelData(summaryRes.channel_breakdown);
        setSeverities(summaryRes.severity_breakdown);
        setOutcomes(summaryRes.outcome_breakdown);
        setExposureData(exposureRes);
      } catch (err) {
        console.error('Failed to load analytics:', err);
      } finally {
        setIsLoading(false);
      }
    };
    loadAnalytics();
  }, []);

  const formatINR = (val: number) => {
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

  const severityColors: Record<string, string> = {
    CRITICAL: '#F43F5E',
    HIGH: '#F59E0B',
    MEDIUM: '#06B6D4',
    LOW: '#10B981',
  };

  const outcomeColors: Record<string, string> = {
    CONFIRMED_FRAUD: '#F43F5E',
    FALSE_POSITIVE: '#10B981',
    INCONCLUSIVE: '#94A3B8',
    PENDING: '#F59E0B',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight">Risk Analytics & Exposure Reports</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Aggregated metrics derived from Oracle SQL group-by queries and VW_CUSTOMER_FRAUD_EXPOSURE view
          </p>
        </div>
      </div>

      {/* Grid of Analytical Breakdowns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Severity Distribution */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-sm font-semibold text-white tracking-wide">
            Surveillance Severity Distribution
          </h2>
          <p className="text-xs text-slate-400 mt-0.5 mb-4">
            Alert counts categorized by automated rule severity level
          </p>

          <div className="h-56 w-full flex items-center justify-center">
            {severities.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={severities} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <XAxis type="number" stroke="#475569" fontSize={11} />
                  <YAxis dataKey="severity" type="category" stroke="#475569" fontSize={11} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0F172A',
                      borderColor: '#334155',
                      borderRadius: '8px',
                      fontSize: '12px',
                    }}
                  />
                  <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                    {severities.map((entry, index) => (
                      <Cell
                        key={`sev-${index}`}
                        fill={severityColors[entry.severity] || '#3B82F6'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-slate-500 font-mono">No severity records.</p>
            )}
          </div>
        </div>

        {/* Investigation Resolution Outcomes */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-sm font-semibold text-white tracking-wide">
            Investigation Resolution Ratio
          </h2>
          <p className="text-xs text-slate-400 mt-0.5 mb-4">
            Case closure distribution across confirmed fraud vs false positives
          </p>

          <div className="h-56 w-full flex items-center justify-center">
            {outcomes.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={outcomes} layout="vertical" margin={{ top: 5, right: 30, left: 30, bottom: 5 }}>
                  <XAxis type="number" stroke="#475569" fontSize={11} />
                  <YAxis dataKey="outcome" type="category" stroke="#475569" fontSize={10} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0F172A',
                      borderColor: '#334155',
                      borderRadius: '8px',
                      fontSize: '12px',
                    }}
                  />
                  <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                    {outcomes.map((entry, index) => (
                      <Cell
                        key={`out-${index}`}
                        fill={outcomeColors[entry.outcome] || '#8B5CF6'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-slate-500 font-mono">No outcomes recorded.</p>
            )}
          </div>
        </div>
      </div>

      {/* Customer Risk Exposure View (Backed by Oracle VW_CUSTOMER_FRAUD_EXPOSURE) */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h2 className="text-sm font-semibold text-white tracking-wide">
              Customer Risk Exposure Ledger
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Live SQL view: <span className="font-mono text-cyan-400">VW_CUSTOMER_FRAUD_EXPOSURE</span>
            </p>
          </div>
          <span className="text-xs font-mono text-slate-500">
            Sorted by Risk Score (Descending)
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-mono">
                <th className="pb-3 font-semibold">Customer ID</th>
                <th className="pb-3 font-semibold">Customer Name</th>
                <th className="pb-3 font-semibold">KYC Status</th>
                <th className="pb-3 font-semibold">Risk Score</th>
                <th className="pb-3 font-semibold">Accounts</th>
                <th className="pb-3 font-semibold">Total Transacted Volume</th>
                <th className="pb-3 font-semibold">Tx Count</th>
                <th className="pb-3 font-semibold text-right">Alerts Incurred</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {exposureData.map((c) => (
                <tr key={c.customer_id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 font-mono font-bold text-cyan-400">#{c.customer_id}</td>
                  <td className="py-3 font-medium text-slate-200">{c.customer_name}</td>
                  <td className="py-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold ${
                        c.kyc_status === 'VERIFIED'
                          ? 'bg-emerald-500/15 text-emerald-400'
                          : c.kyc_status === 'REJECTED'
                          ? 'bg-rose-500/15 text-rose-400'
                          : 'bg-amber-500/15 text-amber-400'
                      }`}
                    >
                      {c.kyc_status}
                    </span>
                  </td>
                  <td className="py-3 font-mono">
                    <div className="flex items-center gap-2">
                      <span
                        className={`font-bold ${
                          c.risk_score >= 70
                            ? 'text-rose-400'
                            : c.risk_score >= 40
                            ? 'text-amber-400'
                            : 'text-emerald-400'
                        }`}
                      >
                        {c.risk_score}/100
                      </span>
                    </div>
                  </td>
                  <td className="py-3 font-mono text-slate-300">{c.total_accounts}</td>
                  <td className="py-3 font-mono font-bold text-white">
                    {formatINR(c.total_transacted_volume)}
                  </td>
                  <td className="py-3 font-mono text-slate-300">{c.total_tx_count}</td>
                  <td className="py-3 font-mono font-bold text-right">
                    {c.alerts_incurred > 0 ? (
                      <span className="text-rose-400 px-2 py-0.5 rounded bg-rose-500/15 border border-rose-500/20">
                        {c.alerts_incurred} Alerts
                      </span>
                    ) : (
                      <span className="text-slate-500">0</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

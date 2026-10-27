import React, { useState, useEffect } from 'react';
import { Navbar } from './components/common/Navbar';
import { Sidebar, NavTab } from './components/common/Sidebar';
import { DashboardPage } from './pages/DashboardPage';
import { TransactionsPage } from './pages/TransactionsPage';
import { AlertsCenterPage } from './pages/AlertsCenterPage';
import { InvestigationsPage } from './pages/InvestigationsPage';
import { AuditTrailPage } from './pages/AuditTrailPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SystemHealthPage } from './pages/SystemHealthPage';
import { DemoWalkthroughPage } from './pages/DemoWalkthroughPage';
import { SystemHealth, DashboardSummary, TrendItem, ChannelMetric, Alert } from './types';
import { api } from './api/client';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<NavTab>('dashboard');
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [trends, setTrends] = useState<TrendItem[]>([]);
  const [channels, setChannels] = useState<ChannelMetric[]>([]);
  const [recentAlerts, setRecentAlerts] = useState<Alert[]>([]);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [openCreateTxModal, setOpenCreateTxModal] = useState<boolean>(false);

  const refreshAllData = async () => {
    try {
      setIsRefreshing(true);
      const [healthData, summaryData, trendsData, analyticsData, alertsData] = await Promise.all([
        api.getHealth().catch(() => null),
        api.getDashboardSummary().catch(() => null),
        api.getDashboardTrends().catch(() => []),
        api.getAnalyticsSummary().catch(() => null),
        api.getAlerts({ page: 1, page_size: 5 }).catch(() => ({ items: [], total: 0 })),
      ]);

      if (healthData) setHealth(healthData);
      if (summaryData) setSummary(summaryData);
      if (trendsData) setTrends(trendsData);
      if (analyticsData) setChannels(analyticsData.channel_breakdown);
      if (alertsData) setRecentAlerts(alertsData.items);
    } catch (err) {
      console.error('Failed refreshing data:', err);
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    refreshAllData();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950">
      {/* Top Navbar */}
      <Navbar
        health={health}
        onRefresh={refreshAllData}
        isRefreshing={isRefreshing}
        onStartDemo={() => setCurrentTab('demo')}
      />

      {/* Main Body with Sidebar + Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          currentTab={currentTab}
          onSelectTab={setCurrentTab}
          pendingAlertsCount={summary?.pending_alerts}
          openInvestigationsCount={summary?.open_investigations}
        />

        {/* Dynamic Page View */}
        <main className="flex-1 overflow-y-auto p-6 lg:p-8 bg-slate-950">
          <div className="max-w-7xl mx-auto">
            {currentTab === 'dashboard' && (
              <DashboardPage
                summary={summary}
                trends={trends}
                channels={channels}
                recentAlerts={recentAlerts}
                onNavigate={setCurrentTab}
                onOpenCreateTransaction={() => {
                  setCurrentTab('transactions');
                  setOpenCreateTxModal(true);
                }}
              />
            )}

            {currentTab === 'transactions' && (
              <TransactionsPage
                onRefreshTrigger={refreshAllData}
                openCreateModal={openCreateTxModal}
                onCloseCreateModal={() => setOpenCreateTxModal(false)}
              />
            )}

            {currentTab === 'alerts' && (
              <AlertsCenterPage
                onNavigateToInvestigations={() => setCurrentTab('investigations')}
                onRefreshTrigger={refreshAllData}
              />
            )}

            {currentTab === 'investigations' && (
              <InvestigationsPage onRefreshTrigger={refreshAllData} />
            )}

            {currentTab === 'audit' && <AuditTrailPage />}

            {currentTab === 'analytics' && <AnalyticsPage />}

            {currentTab === 'health' && <SystemHealthPage />}

            {currentTab === 'demo' && (
              <DemoWalkthroughPage
                onNavigate={setCurrentTab}
                onRefreshTrigger={refreshAllData}
              />
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default App;

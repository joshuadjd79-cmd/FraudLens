import React from 'react';
import {
  LayoutDashboard,
  ArrowLeftRight,
  ShieldAlert,
  Briefcase,
  History,
  BarChart3,
  Server,
  PlaySquare,
  GraduationCap,
} from 'lucide-react';

export type NavTab =
  | 'dashboard'
  | 'transactions'
  | 'alerts'
  | 'investigations'
  | 'audit'
  | 'analytics'
  | 'health'
  | 'demo';

interface SidebarProps {
  currentTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  pendingAlertsCount?: number;
  openInvestigationsCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onSelectTab,
  pendingAlertsCount = 0,
  openInvestigationsCount = 0,
}) => {
  const navItems = [
    {
      id: 'dashboard' as NavTab,
      label: 'Dashboard',
      icon: LayoutDashboard,
      description: 'Executive KPIs & Volume Trends',
    },
    {
      id: 'transactions' as NavTab,
      label: 'Transactions',
      icon: ArrowLeftRight,
      description: 'Real-time Ledger & Filters',
    },
    {
      id: 'alerts' as NavTab,
      label: 'Alerts Center',
      icon: ShieldAlert,
      badge: pendingAlertsCount,
      badgeColor: 'bg-rose-500/20 text-rose-400 border border-rose-500/30',
      description: 'Rule-based Flagged Activity',
    },
    {
      id: 'investigations' as NavTab,
      label: 'Investigations',
      icon: Briefcase,
      badge: openInvestigationsCount,
      badgeColor: 'bg-amber-500/20 text-amber-400 border border-amber-500/30',
      description: 'Case Dockets & Assignments',
    },
    {
      id: 'audit' as NavTab,
      label: 'Audit Trail',
      icon: History,
      description: 'Trigger-Captured Row Mutations',
    },
    {
      id: 'analytics' as NavTab,
      label: 'Analytics & Risk',
      icon: BarChart3,
      description: 'Customer Exposure & Breakdowns',
    },
    {
      id: 'health' as NavTab,
      label: 'System & DB Health',
      icon: Server,
      description: 'Oracle 26ai Diagnostic Monitor',
    },
    {
      id: 'demo' as NavTab,
      label: 'Live Demo Script',
      icon: PlaySquare,
      isSpecial: true,
      description: '8-Step Professor Walkthrough',
    },
  ];

  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800/80 flex flex-col justify-between shrink-0 h-[calc(100vh-4rem)]">
      <div className="p-4 space-y-1.5 overflow-y-auto">
        <p className="px-3 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
          Core Operations
        </p>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              className={`w-full group flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? item.isSpecial
                    ? 'bg-gradient-to-r from-cyan-950/80 to-blue-950/80 text-cyan-300 border border-cyan-500/40 shadow-sm'
                    : 'bg-slate-900 text-cyan-400 border border-slate-700 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-3">
                <div
                  className={`p-1.5 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-cyan-500/10 text-cyan-400'
                      : 'text-slate-400 group-hover:text-slate-200 group-hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>
                <div className="text-left">
                  <div className="font-medium text-slate-200">{item.label}</div>
                  <div className="text-[10px] text-slate-400 font-normal truncate max-w-[120px]">
                    {item.description}
                  </div>
                </div>
              </div>

              {item.badge !== undefined && item.badge > 0 && (
                <span
                  className={`px-1.5 py-0.5 rounded-full text-[10px] font-mono font-bold ${item.badgeColor}`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* College Examination Badge Footer */}
      <div className="p-4 border-t border-slate-900 bg-slate-950/60">
        <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-semibold text-slate-200">
              VIT Vellore Case Study
            </div>
            <div className="text-[10px] text-slate-400">
              D Joshua Daniel & M Saryu
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

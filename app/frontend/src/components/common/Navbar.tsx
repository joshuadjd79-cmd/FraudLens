import React from 'react';
import {
  ShieldAlert,
  Database,
  RefreshCw,
  Play,
  Activity,
  CheckCircle2,
  AlertTriangle,
} from 'lucide-react';
import { SystemHealth } from '../../types';

interface NavbarProps {
  health: SystemHealth | null;
  onRefresh: () => void;
  isRefreshing: boolean;
  onStartDemo: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  health,
  onRefresh,
  isRefreshing,
  onStartDemo,
}) => {
  const isOracleLive = health?.database?.connected ?? false;

  return (
    <header className="sticky top-0 z-40 w-full h-16 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80 px-6 flex items-center justify-between">
      {/* Brand & Left Badges */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 border border-cyan-400/30">
            <ShieldAlert className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-cyan-300 bg-clip-text text-transparent">
                FraudLens
              </span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-mono">
                DBMS v2.0
              </span>
            </div>
            <p className="text-[10px] text-slate-400 hidden sm:block">
              Financial Transaction Monitoring & Investigation Platform
            </p>
          </div>
        </div>

        {/* Vertical divider */}
        <div className="h-6 w-px bg-slate-800 mx-1 hidden md:block" />

        {/* Database Connection Pill */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-mono">
          <Database className={`w-3.5 h-3.5 ${isOracleLive ? 'text-cyan-400' : 'text-amber-400'}`} />
          <span className="text-slate-400">DB:</span>
          {isOracleLive ? (
            <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Oracle 26ai (FREEPDB1)
            </span>
          ) : (
            <span className="flex items-center gap-1.5 text-amber-400 font-medium">
              <AlertTriangle className="w-3 h-3" />
              Demo Memory Engine
            </span>
          )}
        </div>

        {/* Configured Threshold Pill */}
        <div className="hidden lg:flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900/60 border border-slate-800 text-xs font-mono text-slate-300">
          <Activity className="w-3.5 h-3.5 text-blue-400" />
          <span>Surveillance Tier:</span>
          <span className="text-cyan-400 font-semibold">
            ₹{health?.high_amount_threshold?.toLocaleString('en-IN') || '50,000'}
          </span>
        </div>
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-3">
        {/* Interactive Demo Mode CTA */}
        <button
          onClick={onStartDemo}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-semibold text-xs tracking-wide shadow-md shadow-cyan-500/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
          title="Run 8-Step Interactive Professor Demo"
        >
          <Play className="w-3.5 h-3.5 fill-current" />
          <span className="hidden sm:inline">1-Click Live Demo</span>
          <span className="sm:hidden">Demo</span>
        </button>

        {/* Refresh Button */}
        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 transition-colors"
          title="Refresh All Database Views"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-cyan-400' : ''}`} />
        </button>

        {/* Administrator Profile */}
        <div className="flex items-center gap-2.5 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center font-bold text-xs text-white shadow-sm border border-cyan-400/30 font-mono">
            FL
          </div>
          <div className="hidden xl:block text-left">
            <p className="text-xs font-medium text-white">FraudLens Admin</p>
            <p className="text-[10px] text-slate-400">Financial Surveillance Lead</p>
          </div>
        </div>
      </div>
    </header>
  );
};
